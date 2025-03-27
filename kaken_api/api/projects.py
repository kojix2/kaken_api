"""
Projects API module for the KAKEN API client.
"""

import logging
import urllib.parse
from typing import Dict, List, Optional, Union, Any

import requests
import xml.etree.ElementTree as ET

from ..constants import (
    PROJECTS_ENDPOINT,
    DEFAULT_RESULTS_PER_PAGE,
    DEFAULT_LANGUAGE,
    DEFAULT_FORMAT,
    DEFAULT_START_INDEX,
    MAX_PROJECTS_RESULTS,
    FORMAT_XML,
)
from ..exceptions import (
    KakenApiError,
    KakenApiRequestError,
    KakenApiResponseError,
    KakenApiNotFoundError,
)
from ..models import Project, ProjectsResponse
from ..utils import build_url, ensure_list, clean_text, parse_boolean, join_values


logger = logging.getLogger(__name__)


class ProjectsAPI:
    """API client for KAKEN projects."""

    def __init__(self, session: requests.Session, app_id: Optional[str] = None):
        """
        Initialize the ProjectsAPI.

        Args:
            session: The requests session.
            app_id: The application ID for the KAKEN API.
        """
        self.session = session
        self.app_id = app_id

    def search(
        self,
        keyword: Optional[str] = None,
        results_per_page: int = DEFAULT_RESULTS_PER_PAGE,
        language: str = DEFAULT_LANGUAGE,
        start_index: int = DEFAULT_START_INDEX,
        response_format: str = DEFAULT_FORMAT,
        project_title: Optional[str] = None,
        project_number: Optional[str] = None,
        project_type: Optional[Union[str, List[str]]] = None,
        research_category: Optional[str] = None,
        allocation_type: Optional[Union[str, List[str]]] = None,
        research_field: Optional[str] = None,
        institution: Optional[str] = None,
        grant_period_from: Optional[int] = None,
        grant_period_to: Optional[int] = None,
        grant_period_condition: Optional[str] = None,
        total_grant_amount: Optional[str] = None,
        project_status: Optional[Union[str, List[str]]] = None,
        researcher_name: Optional[str] = None,
        researcher_institution: Optional[str] = None,
        researcher_number: Optional[str] = None,
        researcher_role: Optional[Union[str, List[str]]] = None,
        sort_order: Optional[str] = None,
        **kwargs,
    ) -> ProjectsResponse:
        """
        Search for projects.

        Args:
            keyword: Free text search keyword.
            results_per_page: Number of results per page (20, 50, 100, 200, 500).
            language: Response language (ja, en).
            start_index: Start index of results.
            response_format: Response format (html5, xml).
            project_title: Project title.
            project_number: Project number.
            project_type: Project type (project, area, organizer, wrapup, planned, publicly, international).
            research_category: Research category.
            allocation_type: Allocation type (hojokin, kikin, ichibu_kikin).
            research_field: Research field.
            institution: Institution.
            grant_period_from: Grant period from (year).
            grant_period_to: Grant period to (year).
            grant_period_condition: Grant period condition (1: start year, 2: end year, 3: partial period, 4: full period).
            total_grant_amount: Total grant amount (1: < 1M, 2: 1M-5M, 3: 5M-10M, 4: 10M-50M, 5: 50M-100M, 6: 100M-500M, 7: > 500M).
            project_status: Project status (adopted, granted, ceased, suspended, project_closed, declined, discontinued).
            researcher_name: Researcher name.
            researcher_institution: Researcher institution.
            researcher_number: Researcher number.
            researcher_role: Researcher role (principal_investigator, area_organizer, co_investigator_buntan, co_investigator_renkei, research_collaborator, research_fellow, host_researcher, foreign_research_fellow, principal_investigator_support, co_investigator_buntan_support).
            sort_order: Sort order (1: relevance, 2: start year desc, 3: start year asc, 4: total amount desc, 5: total amount asc).
            **kwargs: Additional parameters.

        Returns:
            ProjectsResponse: The search response.
        """
        # Validate parameters
        if not keyword and not any([
            project_title, project_number, project_type, research_category,
            allocation_type, research_field, institution, grant_period_from,
            grant_period_to, total_grant_amount, project_status, researcher_name,
            researcher_institution, researcher_number, researcher_role
        ]):
            raise KakenApiRequestError("Either keyword or at least one search parameter must be provided.")

        if start_index <= 0:
            start_index = DEFAULT_START_INDEX

        if start_index > MAX_PROJECTS_RESULTS:
            raise KakenApiRequestError(f"Start index cannot exceed {MAX_PROJECTS_RESULTS}.")

        if results_per_page not in (20, 50, 100, 200, 500):
            results_per_page = DEFAULT_RESULTS_PER_PAGE

        # Build parameters
        params = {
            "kw": keyword,
            "rw": results_per_page,
            "lang": language,
            "st": start_index,
            "format": response_format,
            "qa": project_title,
            "qb": project_number,
            "c6": join_values(ensure_list(project_type)),
            "qc": research_category,
            "c7": join_values(ensure_list(allocation_type)),
            "qd": research_field,
            "qe": institution,
            "s1": grant_period_from,
            "s2": grant_period_to,
            "o1": grant_period_condition,
            "s3": total_grant_amount,
            "c1": join_values(ensure_list(project_status)),
            "qg": researcher_name,
            "qh": researcher_institution,
            "qm": researcher_number,
            "c2": join_values(ensure_list(researcher_role)),
            "od": sort_order,
            "appid": self.app_id,
        }

        # Add additional parameters
        params.update(kwargs)

        # Build URL
        url = build_url(PROJECTS_ENDPOINT, params)

        try:
            # Make request
            logger.debug(f"Making request to {url}")
            response = self.session.get(url)
            response.raise_for_status()

            # Parse response
            if response_format == FORMAT_XML:
                return self._parse_xml_response(response.content)
            else:
                # For now, we only support XML responses
                raise KakenApiRequestError(f"Unsupported response format: {response_format}")

        except requests.RequestException as e:
            if e.response is not None and e.response.status_code == 404:
                raise KakenApiNotFoundError("Resource not found", response=e.response)
            raise KakenApiRequestError(f"Request failed: {str(e)}", response=getattr(e, "response", None))

    def _parse_xml_response(self, content: bytes) -> ProjectsResponse:
        """
        Parse XML response.

        Args:
            content: The XML content.

        Returns:
            ProjectsResponse: The parsed response.
        """
        try:
            # Parse XML
            root = ET.fromstring(content)

            # Extract metadata
            total_results = root.find("totalResults")
            start_index = root.find("startIndex")
            items_per_page = root.find("itemsPerPage")

            # Create response
            response = ProjectsResponse(
                raw_data=content,
                total_results=int(total_results.text) if total_results is not None else None,
                start_index=int(start_index.text) if start_index is not None else None,
                items_per_page=int(items_per_page.text) if items_per_page is not None else None,
                projects=[],
            )

            # Extract projects
            for grant_award in root.findall(".//grantAward"):
                project = self._parse_project(grant_award)
                response.projects.append(project)

            return response

        except ET.ParseError as e:
            raise KakenApiResponseError(f"Failed to parse XML response: {str(e)}")
        except Exception as e:
            raise KakenApiResponseError(f"Failed to process response: {str(e)}")

    def _parse_project(self, grant_award: ET.Element) -> Project:
        """
        Parse project from XML element.

        Args:
            grant_award: The XML element.

        Returns:
            Project: The parsed project.
        """
        # This is a simplified implementation
        # A complete implementation would parse all fields from the XML
        project = Project(
            id=grant_award.get("id"),
            award_number=grant_award.get("awardNumber"),
            project_type=grant_award.get("projectType"),
            raw_data=ET.tostring(grant_award),
        )

        # Parse title
        summary = grant_award.find(".//summary")
        if summary is not None:
            title = summary.find(".//title")
            if title is not None:
                project.title = clean_text(title.text)

        return project
