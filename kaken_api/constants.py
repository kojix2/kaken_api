"""
Constants for the KAKEN API client.
"""

# API Endpoints
PROJECTS_ENDPOINT = "https://kaken.nii.ac.jp/opensearch/"
RESEARCHERS_ENDPOINT = "https://nrid.nii.ac.jp/opensearch/"

# Default Parameters
DEFAULT_RESULTS_PER_PAGE = 20
DEFAULT_LANGUAGE = "ja"
DEFAULT_FORMAT = "xml"  # For projects
DEFAULT_RESEARCHER_FORMAT = "json"  # For researchers
DEFAULT_START_INDEX = 1

# Maximum Results
MAX_PROJECTS_RESULTS = 200000
MAX_RESEARCHERS_RESULTS = 1000

# Response Formats
FORMAT_HTML = "html5"
FORMAT_XML = "xml"
FORMAT_JSON = "json"

# Languages
LANGUAGE_JAPANESE = "ja"
LANGUAGE_ENGLISH = "en"

# Project Status Codes
PROJECT_STATUS = {
    "adopted": "採択",
    "granted": "交付",
    "ceased": "中断",
    "suspended": "留保",
    "project_closed": "完了",
    "declined": "採択後辞退",
    "discontinued": "中途終了",
}

# Project Types
PROJECT_TYPES = {
    "project": "研究課題",
    "area": "領域",
    "organizer": "総括班",
    "wrapup": "成果取りまとめ",
    "planned": "計画研究",
    "publicly": "公募研究",
    "international": "国際活動支援班",
}

# Allocation Types
ALLOCATION_TYPES = {
    "hojokin": "補助金",
    "kikin": "基金",
    "ichibu_kikin": "一部基金",
}

# Researcher Roles
RESEARCHER_ROLES = {
    "principal_investigator": "研究代表者",
    "area_organizer": "領域代表者",
    "co_investigator_buntan": "研究分担者",
    "co_investigator_renkei": "連携研究者",
    "research_collaborator": "研究協力者",
    "research_fellow": "特別研究員",
    "host_researcher": "受入研究者",
    "foreign_research_fellow": "外国人特別研究員",
    "principal_investigator_support": "研究支援代表者",
    "co_investigator_buntan_support": "研究支援分担者",
}

# Report Types
REPORT_TYPES = {
    "jiseki_hokoku": "実績報告書",
    "jiko_hyoka_hokoku": "自己評価報告書",
    "kenkyu_sinchoku_hyoka": "研究進捗評価",
    "kenkyu_seika_hokoku_gaiyo": "研究成果報告書概要",
    "chukan_hyoka_hokoku": "中間評価報告書",
    "jigo_hyoka_hokoku": "事後評価報告書",
    "jishi_jokyo_hokoku_kikin": "実施状況報告書",
    "kenkyu_seika_hokoku": "研究成果報告書",
    "saitaku_shoken": "審査結果の所見",
    "saitaku_gaiyo": "研究概要(採択時)",
    "kenkyu_shinchoku_hyoka_gaiyo": "研究概要(研究進捗評価)",
    "kenkyu_shinchoku_hyoka_genchi_chosa": "研究進捗評価(現地調査コメント)",
    "kenkyu_shinchoku_hyoka_keka": "研究進捗評価(評価結果)",
    "kenkyu_shinchoku_hyoka_kensho": "研究進捗評価(検証)",
    "tsuiseki_hyoka_shoken": "評価の所見(追跡評価)",
    "tsuiseki_hyoka_jiko_hyoka": "自己評価書(追跡評価)",
    "tsuiseki_hyoka_kenkyu_gaiyo": "研究概要(追跡評価)",
    "chukan_hyoka_shoken": "中間評価(所見)",
    "jigo_hyoka_shoken": "事後評価(所見)",
    "kenkyu_seika_hapyo_hokoku": "研究成果発表報告書",
}

# Product Types
PRODUCT_TYPES = {
    "journal_article": "雑誌論文",
    "presentation": "学会発表",
    "symposium": "学会・シンポジウム開催",
    "book": "図書",
    "press": "プレス/新聞発表",
    "note": "備考",
    "patent": "産業財産権",
    "publication": "文献書誌",
}

# Sort Options for Projects
PROJECT_SORT_OPTIONS = {
    "1": "適合度",
    "2": "研究開始年:新しい順",
    "3": "研究開始年:古い順",
    "4": "配分額合計:多い順",
    "5": "配分額合計:少ない順",
}

# Sort Options for Researchers
RESEARCHER_SORT_OPTIONS = {
    "1": "適合度",
    "2": "研究者氏名のカナ:昇順",
    "3": "研究者氏名のカナ:降順",
    "4": "研究者氏名のアルファベット:昇順",
    "5": "研究者氏名のアルファベット:降順",
    "6": "研究課題数:少ない順",
    "7": "研究課題数:多い順",
}
