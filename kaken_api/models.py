"""
Data models for the KAKEN API client.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Union
from datetime import datetime


@dataclass
class KakenApiResponse:
    """Base class for KAKEN API responses."""
    
    raw_data: Any = field(repr=False)
    total_results: Optional[int] = None
    start_index: Optional[int] = None
    items_per_page: Optional[int] = None


@dataclass
class Institution:
    """Institution information."""
    
    name: str
    code: Optional[str] = None
    type: Optional[str] = None


@dataclass
class Department:
    """Department information."""
    
    name: str
    code: Optional[str] = None


@dataclass
class JobTitle:
    """Job title information."""
    
    name: str
    code: Optional[str] = None


@dataclass
class Affiliation:
    """Affiliation information."""
    
    institution: Optional[Institution] = None
    department: Optional[Department] = None
    job_title: Optional[JobTitle] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


@dataclass
class PersonName:
    """Person name information."""
    
    full_name: str
    family_name: Optional[str] = None
    given_name: Optional[str] = None
    family_name_reading: Optional[str] = None
    given_name_reading: Optional[str] = None


@dataclass
class Researcher:
    """Researcher information."""
    
    id: Optional[str] = None
    name: Optional[PersonName] = None
    affiliations: List[Affiliation] = field(default_factory=list)
    researcher_number: Optional[str] = None
    erad_researcher_number: Optional[str] = None
    jglobal_id: Optional[str] = None
    researchmap_id: Optional[str] = None
    orcid: Optional[str] = None
    projects: List['Project'] = field(default_factory=list)
    products: List['Product'] = field(default_factory=list)
    raw_data: Any = field(default=None, repr=False)


@dataclass
class ResearcherRole:
    """Researcher role information."""
    
    researcher: Researcher
    role: str
    participate: Optional[str] = None


@dataclass
class Category:
    """Category information."""
    
    name: str
    path: Optional[str] = None
    code: Optional[str] = None


@dataclass
class Field:
    """Field information."""
    
    name: str
    path: Optional[str] = None
    code: Optional[str] = None
    field_table: Optional[str] = None


@dataclass
class Keyword:
    """Keyword information."""
    
    text: str
    language: Optional[str] = None


@dataclass
class ProjectStatus:
    """Project status information."""
    
    status_code: str
    date: Optional[datetime] = None
    note: Optional[str] = None


@dataclass
class PeriodOfAward:
    """Period of award information."""
    
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    start_fiscal_year: Optional[int] = None
    end_fiscal_year: Optional[int] = None


@dataclass
class AwardAmount:
    """Award amount information."""
    
    total_cost: Optional[int] = None
    direct_cost: Optional[int] = None
    indirect_cost: Optional[int] = None
    fiscal_year: Optional[int] = None
    currency: Optional[str] = "JPY"
    planned: bool = False


@dataclass
class Project:
    """Project information."""
    
    id: Optional[str] = None
    award_number: Optional[str] = None
    title: Optional[str] = None
    title_en: Optional[str] = None
    title_abbreviated: Optional[str] = None
    categories: List[Category] = field(default_factory=list)
    fields: List[Field] = field(default_factory=list)
    institutions: List[Institution] = field(default_factory=list)
    keywords: List[Keyword] = field(default_factory=list)
    period_of_award: Optional[PeriodOfAward] = None
    project_status: Optional[ProjectStatus] = None
    project_type: Optional[str] = None
    allocation_type: Optional[str] = None
    members: List[ResearcherRole] = field(default_factory=list)
    award_amounts: List[AwardAmount] = field(default_factory=list)
    raw_data: Any = field(default=None, repr=False)


@dataclass
class ProductIdentifier:
    """Product identifier information."""
    
    type: str
    value: str
    authenticated: bool = False


@dataclass
class ProductAuthor:
    """Product author information."""
    
    name: str
    sequence: Optional[int] = None
    researcher_id: Optional[str] = None


@dataclass
class Product:
    """Product information."""
    
    id: Optional[str] = None
    type: Optional[str] = None
    title: Optional[str] = None
    title_en: Optional[str] = None
    authors: List[ProductAuthor] = field(default_factory=list)
    journal_title: Optional[str] = None
    journal_title_en: Optional[str] = None
    volume: Optional[str] = None
    issue: Optional[str] = None
    pages: Optional[str] = None
    publication_date: Optional[datetime] = None
    language: Optional[str] = None
    reviewed: bool = False
    invited: bool = False
    foreign: bool = False
    open_access: bool = False
    acknowledgement: bool = False
    joint_international: bool = False
    identifiers: List[ProductIdentifier] = field(default_factory=list)
    raw_data: Any = field(default=None, repr=False)


@dataclass
class ProjectsResponse(KakenApiResponse):
    """Response for projects search."""
    
    projects: List[Project] = field(default_factory=list)


@dataclass
class ResearchersResponse(KakenApiResponse):
    """Response for researchers search."""
    
    researchers: List[Researcher] = field(default_factory=list)


@dataclass
class ProductsResponse(KakenApiResponse):
    """Response for products search."""
    
    products: List[Product] = field(default_factory=list)
