import pandas as pd
import pytest
from shapely.geometry import Point, LineString


def import_diag():
    import sirs_import.diagnose_mapping as dm
    return dm


# =====================================================================
# UTILITAIRE
# =====================================================================
def _rows_dict(rows):
    """Permet d'accéder aux lignes par clé : rows_by_key['designation']"""
    return {r[0]: r for r in rows}


# =====================================================================
# 1) TESTS : COLONNES TEXTUELLES
# =====================================================================
def test_diag_text_columns_all_present():
    dm = import_diag()
    gdf = pd.DataFrame({
        dm.COL_DESIGNATION: ["aaa"],
        dm.COL_LIBELLE: ["bbb"],
        dm.COL_COMMENTAIRE: ["ccc"],
        dm.COL_LIEUDIT: ["ddd"],
        "geometry": [Point(0, 0)]
    })

    rows, errors, warnings = dm.diagnose_mapping(
        available_cols=list(gdf.columns),
        gdf=gdf,
        gpkg_schema={"geometry": "POINT"},
        user_ids=[]
    )

    R = _rows_dict(rows)

    assert R["designation"][2] == "colonne GPKG"
    assert R["libelle"][2] == "colonne GPKG"
    assert R["commentaire"][2] == "colonne GPKG"
    assert R["lieuDit"][2] == "colonne GPKG"
    assert errors == []


def test_diag_text_columns_missing():
    dm = import_diag()
    gdf = pd.DataFrame({"geometry": [Point(0, 0)]})

    rows, errors, warnings = dm.diagnose_mapping(
        available_cols=["geometry"],
        gdf=gdf,
        gpkg_schema={"geometry": "POINT"},
        user_ids=[]
    )

    R = _rows_dict(rows)

    assert R["designation"][2] == "manquante"
    assert R["libelle"][2] == "manquante"
    assert len(errors) >= 1


# =====================================================================
# 2) TESTS : LINEAR ID
# =====================================================================
def test_linear_id_valid_column():
    dm = import_diag()

    gdf = pd.DataFrame({
        dm.COL_LINEAR_ID: ["11111111-1111-1111-1111-111111111111"],
        "geometry": [Point(0, 0)]
    })

    rows, errors, warnings = dm.diagnose_mapping(
        available_cols=list(gdf.columns),
        gdf=gdf,
        gpkg_schema={"geometry": "POINT"},
        user_ids=[]
    )

    R = _rows_dict(rows)
    assert R["linearId"][4] == "oui"
    assert errors == []


def test_linear_id_invalid_uuid():
    dm = import_diag()

    gdf = pd.DataFrame({
        dm.COL_LINEAR_ID: ["INVALID"],
        "geometry": [Point(0, 0)]
    })

    rows, errors, warnings = dm.diagnose_mapping(
        available_cols=list(gdf.columns),
        gdf=gdf,
        gpkg_schema={"geometry": "POINT"},
        user_ids=[]
    )

    assert len(errors) == 1
    assert "UUID invalides" in errors[0]


def test_linear_id_fallback_uuid(monkeypatch):
    dm = import_diag()

    monkeypatch.setattr(dm, "COL_LINEAR_ID", "22222222-2222-2222-2222-222222222222")

    gdf = pd.DataFrame({"geometry": [Point(1, 1)]})

    rows, errors, warnings = dm.diagnose_mapping(
        available_cols=["geometry"],
        gdf=gdf,
        gpkg_schema={"geometry": "POINT"},
        user_ids=[]
    )

    R = _rows_dict(rows)
    assert R["linearId"][4] == "oui"
    assert errors == []


# =====================================================================
# 3) TESTS : AUTHOR
# =====================================================================
def test_author_from_column(monkeypatch):
    dm = import_diag()

    monkeypatch.setattr(dm, "COL_AUTHOR", "author_col")

    gdf = pd.DataFrame({
        "author_col": ["11111111-1111-1111-1111-111111111111"],
        "geometry": [Point(0, 0)]
    })

    rows, errors, warnings = dm.diagnose_mapping(
        available_cols=list(gdf.columns),
        gdf=gdf,
        gpkg_schema={"geometry": "POINT"},
        user_ids=["11111111-1111-1111-1111-111111111111"]
    )

    R = _rows_dict(rows)
    assert R["author"][4] == "oui"
    assert errors == []


def test_author_invalid_sirs(monkeypatch):
    dm = import_diag()

    monkeypatch.setattr(dm, "COL_AUTHOR", "author_col")

    gdf = pd.DataFrame({
        "author_col": ["11111111-1111-1111-1111-111111111111"],
        "geometry": [Point(0, 0)]
    })

    rows, errors, warnings = dm.diagnose_mapping(
        available_cols=list(gdf.columns),
        gdf=gdf,
        gpkg_schema={"geometry": "POINT"},
        user_ids=[]  # inconnu
    )

    assert len(errors) == 1
    assert "UUID inconnus" in errors[0]


# =====================================================================
# 4) TESTS : CODES STANDARD (sourceId, coteId, positionId)
# =====================================================================
def test_source_column_valid(monkeypatch):
    dm = import_diag()

    monkeypatch.setattr(dm, "COL_SOURCE_ID", "src")
    gdf = pd.DataFrame({
        "src": ["RefSource:3"],
        "geometry": [Point(0, 0)]
    })

    rows, errors, warnings = dm.diagnose_mapping(
        available_cols=list(gdf.columns),
        gdf=gdf,
        gpkg_schema={"geometry": "POINT"},
        user_ids=[]
    )

    R = _rows_dict(rows)
    assert R["sourceId"][4] == "oui"


def test_source_invalid(monkeypatch):
    dm = import_diag()

    monkeypatch.setattr(dm, "COL_SOURCE_ID", "src")
    gdf = pd.DataFrame({
        "src": ["BAD_CODE"],
        "geometry": [Point(0, 0)]
    })

    rows, errors, warnings = dm.diagnose_mapping(
        available_cols=list(gdf.columns),
        gdf=gdf,
        gpkg_schema={"geometry": "POINT"},
        user_ids=[]
    )

    assert len(errors) == 1


# =====================================================================
# 5) GÉOMÉTRIE + INTERACTION UTILISATEUR
# =====================================================================
def test_geometry_point():
    dm = import_diag()

    gdf = pd.DataFrame({"geometry": [Point(1, 2)]})

    rows, errors, warnings = dm.diagnose_mapping(
        available_cols=["geometry"],
        gdf=gdf,
        gpkg_schema={"geometry": "POINT"},
        user_ids=[]
    )

    R = _rows_dict(rows)
    assert "positionDebut" in R
    assert "positionFin" in R


def test_geometry_linestring_accept(monkeypatch):
    dm = import_diag()

    gdf = pd.DataFrame({
        "geometry": [LineString([(0,0), (1,1), (2,2)])]
    })

    monkeypatch.setattr("builtins.input", lambda _: "1")

    rows, errors, warnings = dm.diagnose_mapping(
        available_cols=["geometry"],
        gdf=gdf,
        gpkg_schema={"geometry": "LINESTRING"},
        user_ids=[]
    )

    R = _rows_dict(rows)
    assert "positionDebut" in R
    assert errors == []


def test_geometry_linestring_cancel(monkeypatch):
    dm = import_diag()
    from sirs_import.exceptions import UserCancelled

    gdf = pd.DataFrame({
        "geometry": [LineString([(0,0), (1,1)])]
    })

    monkeypatch.setattr("builtins.input", lambda _: "2")

    with pytest.raises(UserCancelled):
        dm.diagnose_mapping(
            available_cols=["geometry"],
            gdf=gdf,
            gpkg_schema={"geometry": "LINESTRING"},
            user_ids=[]
        )


# =====================================================================
# 6) DATES
# =====================================================================
def test_dates_valid():
    dm = import_diag()

    gdf = pd.DataFrame({
        dm.COL_DATE_DEBUT: [pd.Timestamp("2023-01-01")],
        dm.COL_DATE_FIN: [pd.Timestamp("2023-01-10")],
        "geometry": [Point(0,0)],
    })

    gpkg_schema = {
        dm.COL_DATE_DEBUT: "date",
        dm.COL_DATE_FIN: "date",
        "geometry": "POINT",
    }

    rows, errors, warnings = dm.diagnose_mapping(
        available_cols=list(gdf.columns),
        gdf=gdf,
        gpkg_schema=gpkg_schema,
        user_ids=[]
    )

    assert errors == []


def test_dates_inconsistent():
    dm = import_diag()

    gdf = pd.DataFrame({
        dm.COL_DATE_DEBUT: [pd.Timestamp("2023-01-10")],
        dm.COL_DATE_FIN: [pd.Timestamp("2023-01-01")],
        "geometry": [Point(0,0)],
    })

    gpkg_schema = {
        dm.COL_DATE_DEBUT: "date",
        dm.COL_DATE_FIN: "date",
        "geometry": "POINT",
    }

    rows, errors, warnings = dm.diagnose_mapping(
        available_cols=list(gdf.columns),
        gdf=gdf,
        gpkg_schema=gpkg_schema,
        user_ids=[]
    )

    assert len(errors) >= 1
    assert any("date_fin" in err for err in errors)


# =====================================================================
# 7) USED_COLUMNS
# =====================================================================
def test_used_columns_tracking(monkeypatch):
    dm = import_diag()

    # Reset l’état
    dm.USED_COLUMNS.clear()

    gdf = pd.DataFrame({
        dm.COL_DESIGNATION: ["D"],
        dm.COL_LIBELLE: ["L"],
        "geometry": [Point(0,0)]
    })

    dm.diagnose_mapping(
        available_cols=list(gdf.columns),
        gdf=gdf,
        gpkg_schema={"geometry": "POINT"},
        user_ids=[]
    )

    assert dm.COL_DESIGNATION in dm.USED_COLUMNS
    assert dm.COL_LIBELLE in dm.USED_COLUMNS

