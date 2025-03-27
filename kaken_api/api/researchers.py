"""
Researchers API module for the KAKEN API client.
"""

import logging
import json
from typing import Dict, List, Optional, Union, Any

import requests

from ..constants import (
    RESEARCHERS_ENDPOINT,
    DEFAULT_RESULTS_PER_PAGE,
    DEFAULT_LANGUAGE,
    DEFAULT_RESEARCHER_FORMAT,
    DEFAULT_START_INDEX,
    MAX_RESEARCHERS_RESULTS,
    FORMAT_JSON,
)
from ..exceptions import (
    KakenApiError,
    KakenApiRequestError,
    KakenApiResponseError,
    KakenApiNotFoundError,
)
from ..models import Researcher, ResearchersResponse, PersonName, Affiliation, Institution, Department, JobTitle
from ..utils import build_url, ensure_list, clean_text, parse_boolean, join_values


logger = logging.getLogger(__name__)


class ResearchersAPI:
    """API client for KAKEN researchers."""

    def __init__(self, session: requests.Session, app_id: Optional[str] = None):
        """
        Initialize the ResearchersAPI.

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
        response_format: str = DEFAULT_RESEARCHER_FORMAT,
        researcher_name: Optional[str] = None,
        researcher_number: Optional[str] = None,
        researcher_institution: Optional[str] = None,
        researcher_department: Optional[str] = None,
        researcher_job_title: Optional[str] = None,
        project_title: Optional[str] = None,
        project_number: Optional[str] = None,
        research_category: Optional[str] = None,
        research_field: Optional[str] = None,
        institution: Optional[str] = None,
        grant_period_from: Optional[int] = None,
        grant_period_to: Optional[int] = None,
        grant_period_condition: Optional[str] = None,
        sort_order: Optional[str] = None,
        **kwargs,
    ) -> ResearchersResponse:
        """
        Search for researchers.

        Args:
            keyword: Free text search keyword.
            results_per_page: Number of results per page (20, 50, 100, 200, 500).
            language: Response language (ja, en).
            start_index: Start index of results.
            response_format: Response format (html5, json).
            researcher_name: Researcher name.
            researcher_number: Researcher number.
            researcher_institution: Researcher institution.
            researcher_department: Researcher department.
            researcher_job_title: Researcher job title.
            project_title: Project title.
            project_number: Project number.
            research_category: Research category.
            research_field: Research field.
            institution: Institution.
            grant_period_from: Grant period from (year).
            grant_period_to: Grant period to (year).
            grant_period_condition: Grant period condition (1: start year, 2: end year, 3: partial period, 4: full period).
            sort_order: Sort order (1: relevance, 2: name kana asc, 3: name kana desc, 4: name alphabet asc, 5: name alphabet desc, 6: project count asc, 7: project count desc).
            **kwargs: Additional parameters.

        Returns:
            ResearchersResponse: The search response.
        """
        # Validate parameters
        if not keyword and not any([
            researcher_name, researcher_number, researcher_institution,
            researcher_department, researcher_job_title, project_title,
            project_number, research_category, research_field, institution,
            grant_period_from, grant_period_to
        ]):
            raise KakenApiRequestError("Either keyword or at least one search parameter must be provided.")

        if start_index <= 0:
            start_index = DEFAULT_START_INDEX

        if start_index > MAX_RESEARCHERS_RESULTS:
            raise KakenApiRequestError(f"Start index cannot exceed {MAX_RESEARCHERS_RESULTS}.")

        if results_per_page not in (20, 50, 100, 200, 500):
            results_per_page = DEFAULT_RESULTS_PER_PAGE

        # Build parameters
        params = {
            "kw": keyword,
            "rw": results_per_page,
            "lang": language,
            "st": start_index,
            "format": response_format,
            "qg": researcher_name,
            "qm": researcher_number,
            "qh": researcher_institution,
            "qq": researcher_department,
            "qs": researcher_job_title,
            "qa": project_title,
            "qb": project_number,
            "qc": research_category,
            "qd": research_field,
            "qe": institution,
            "s1": grant_period_from,
            "s2": grant_period_to,
            "o1": grant_period_condition,
            "od": sort_order,
            "appid": self.app_id,
        }

        # Add additional parameters
        params.update(kwargs)

        # Build URL
        url = build_url(RESEARCHERS_ENDPOINT, params)

        try:
            # Make request
            logger.debug(f"Making request to {url}")
            response = self.session.get(url)
            response.raise_for_status()

            # Parse response
            if response_format == FORMAT_JSON:
                return self._parse_json_response(response.content)
            else:
                # For now, we only support JSON responses
                raise KakenApiRequestError(f"Unsupported response format: {response_format}")

        except requests.RequestException as e:
            if e.response is not None and e.response.status_code == 404:
                raise KakenApiNotFoundError("Resource not found", response=e.response)
            raise KakenApiRequestError(f"Request failed: {str(e)}", response=getattr(e, "response", None))

    def _parse_json_response(self, content: bytes) -> ResearchersResponse:
        """
        Parse JSON response.

        Args:
            content: The JSON content.

        Returns:
            ResearchersResponse: The parsed response.
        """
        try:
            # Parse JSON
            data = json.loads(content)

            # Create response
            response = ResearchersResponse(
                raw_data=data,
                total_results=data.get("totalResults"),
                start_index=data.get("startIndex"),
                items_per_page=data.get("itemsPerPage"),
                researchers=[],
            )

            # Extract researchers
            for researcher_data in data.get("researchers", []):
                researcher = self._parse_researcher(researcher_data)
                response.researchers.append(researcher)

            return response

        except json.JSONDecodeError as e:
            raise KakenApiResponseError(f"Failed to parse JSON response: {str(e)}")
        except Exception as e:
            raise KakenApiResponseError(f"Failed to process response: {str(e)}")

    def _parse_researcher(self, data: Dict) -> Researcher:
        """
        Parse researcher from JSON data.

        Args:
            data: The JSON data.

        Returns:
            Researcher: The parsed researcher.
        """
        # This is a simplified implementation
        # A complete implementation would parse all fields from the JSON
        researcher = Researcher(
            id=data.get("accn"),
            raw_data=data,
        )

        # Parse name
        name_data = data.get("name", {})
        if name_data:
            family_name = None
            given_name = None
            
            # Extract family name
            family_names = name_data.get("name:familyName", [])
            if family_names:
                for name in family_names:
                    if name.get("lang") == "ja":
                        family_name = name.get("text")
                        break
            
            # Extract given name
            given_names = name_data.get("name:givenName", [])
            if given_names:
                for name in given_names:
                    if name.get("lang") == "ja":
                        given_name = name.get("text")
                        break
            
            # Create person name
            full_name = f"{family_name} {given_name}" if family_name and given_name else None
            researcher.name = PersonName(
                full_name=full_name or "Unknown",
                family_name=family_name,
                given_name=given_name,
            )

        # Parse current affiliations
        current_affiliations = data.get("affiliations:current", [])
        for affiliation_data in current_affiliations:
            institution_data = affiliation_data.get("affiliation:institution", {})
            department_data = affiliation_data.get("affiliation:department", {})
            job_title_data = affiliation_data.get("affiliation:jobTitle", {})
            
            # Create institution
            institution = None
            if institution_data:
                institution_values = institution_data.get("humanReadableValue", [])
                institution_name = None
                for value in institution_values:
                    if value.get("lang") == "ja":
                        institution_name = value.get("text")
                        break
                
                if institution_name:
                    institution = Institution(
                        name=institution_name,
                        code=institution_data.get("id:institution:kakenhi"),
                        type=institution_data.get("category:institution:kakenhi"),
                    )
            
            # Create department
            department = None
            if department_data:
                department_values = department_data.get("humanReadableValue", [])
                department_name = None
                for value in department_values:
                    if value.get("lang") == "ja":
                        department_name = value.get("text")
                        break
                
                if department_name:
                    department = Department(
                        name=department_name,
                        code=department_data.get("id:department:mext"),
                    )
            
            # Create job title
            job_title = None
            if job_title_data:
                job_title_values = job_title_data.get("humanReadableValue", [])
                job_title_name = None
                for value in job_title_values:
                    if value.get("lang") == "ja":
                        job_title_name = value.get("text")
                        break
                
                if job_title_name:
                    job_title = JobTitle(
                        name=job_title_name,
                        code=job_title_data.get("id:jobTitle:mext"),
                    )
            
            # Create affiliation
            if institution or department or job_title:
                affiliation = Affiliation(
                    institution=institution,
                    department=department,
                    job_title=job_title,
                )
                researcher.affiliations.append(affiliation)

        return researcher
