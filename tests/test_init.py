"""Test main functions."""
from freezegun import freeze_time
import datetime
import logging
import pytest
import openeihttp

from openeihttp import InvalidCall


def test_get_lookup_data(test_lookup, lookup_mock):
    """Test v4 Status reply"""
    status = test_lookup.lookup_plans()
    assert status == {
        "Arizona Public Service Co": [
            {"name": "Time Advantage 7pm to noon", "label": "539fba68ec4f024bc1dc2db3"},
            {
                "name": "Residential Bundled & Adjustments No Tax TOU; Time Adv Super peak 7PM-Noon (ET-SP)",
                "label": "542aec8a5257a310694b1ab6",
            },
            {
                "name": "Residential Service Bundled Standard rate",
                "label": "55563ddf5457a3bf6c8b4570",
            },
            {
                "name": "Residential Bundled & Adjustments No Tax TOU ; Time Adv 7PM-Noon  (ET-2)",
                "label": "55563df55457a35e758b4568",
            },
            {
                "name": "Residential Bundled & Adjustments No Tax TOU w/ Demand; Combined Adv  7PM-Noon (ECT-2)",
                "label": "562bea025457a31838418740",
            },
            {
                "name": "Residential Service Bundled Standard rate",
                "label": "5743aa135457a3a636906f5b",
            },
            {
                "name": "Residential Service TOU Time Advantage 7PM-Noon (ET-2)",
                "label": "574613aa5457a3557e906f5b",
            },
            {
                "name": "Residential Service TOU Combined Advantage 7PM-Noon  (ECT-2)",
                "label": "574615f85457a3557e906f5c",
            },
            {
                "name": "Residential Service Standard (E-12)",
                "label": "5748ab725457a37e7d906f5b",
            },
            {
                "name": "Residential Service TOU Time Advantage 7PM-Noon (ET-2)",
                "label": "5748ac7a5457a37d7d906f5b",
            },
            {
                "name": "Residential Service Standard (E-12)",
                "label": "5881345e5457a35973316ce7",
            },
            {
                "name": "Residential Service TOU Time Advantage 7PM-Noon (ET-2)",
                "label": "588135ee5457a3873f316ce6",
            },
            {
                "name": "Residential Service TOU Combined Advantage 7PM-Noon  (ECT-2)",
                "label": "5890c92f5457a36c373dbec0",
            },
            {
                "name": "Residential Service Standard (E-12) Low Income",
                "label": "59fcde8e5457a3a04cc05084",
            },
            {
                "name": "Residential Service Standard (E-12) [Frozen]",
                "label": "5a592dee5457a3931d423a81",
            },
            {
                "name": "Residential Service TOU Time Advantage 7PM-Noon (ET-2) [Frozen]",
                "label": "5a5930055457a36274423a7d",
            },
            {
                "name": "Residential Service TOU Combined Advantage 7PM-Noon  (ECT-2) [Frozen]",
                "label": "5a5930bf5457a3371c423a7e",
            },
            {
                "name": "Residential Time of Use (Saver Choice)",
                "label": "5a5933d25457a3ad69423a81",
            },
            {
                "name": "Residential Service (Saver Choice Plus)",
                "label": "5a5935475457a3ad69423a82",
            },
            {
                "name": "Residential Service (Saver Choice Max)",
                "label": "5a5936ef5457a36274423a7f",
            },
            {
                "name": "Extra Small Residential Service (Lite Choice)",
                "label": "5a5937bb5457a3b71c423a7f",
            },
            {
                "name": "Small Residential Service (Premier Choice)",
                "label": "5a59388c5457a3931d423a84",
            },
            {
                "name": "Large Residential Service (Premier Choice Large)",
                "label": "5a5939515457a3371c423a7f",
            },
            {
                "name": "Residential Service (Pilot Technology Rate)",
                "label": "5a593d815457a3371c423a80",
            },
            {
                "name": "Extra Small Residential Service (Lite Choice) R-XS",
                "label": "5cacc5605457a379257780e2",
            },
            {
                "name": "Small Residential Service (Premier Choice) R-Basic",
                "label": "5cacc6545457a3634c7780e2",
            },
            {
                "name": "Large Residential Service (Premier Choice Large) R-Basic L [Frozen]",
                "label": "5cacc6e75457a3a8497780e2",
            },
            {
                "name": "Residential Time of Use (Saver Choice) TOU-E",
                "label": "5cacc7715457a393487780e2",
            },
            {
                "name": "Residential Service (Saver Choice Max)",
                "label": "5cacc9ae5457a3c6517780e2",
            },
            {
                "name": "Residential Service (Saver Choice Plus) R-2",
                "label": "5cacc9d15457a31d537780e2",
            },
            {
                "name": "Residential Service (Saver Choice Max) R-3",
                "label": "5caccb2f5457a3c8517780e2",
            },
            {
                "name": "Residential Service (Pilot Technology Rate) R-Tech",
                "label": "5caccd925457a31a537780e2",
            },
        ],
        "Not Listed": [{"label": "Not Listed", "name": "Not Listed"}],
    }


@freeze_time("2021-08-13 10:21:34")
def test_get_rate_data(test_rates, plandata_mock, caplog):
    """Test rate schedules."""
    with caplog.at_level(logging.DEBUG):
        test_rates.update()
    status = test_rates.current_rate
    assert status == 0.06118
    assert "No data populated, refreshing data." in caplog.text


@freeze_time("2021-08-13 13:20:00")
def test_get_rate_data_2(test_rates, plandata_mock):
    """Test rate schedules."""
    test_rates.update()
    status = test_rates.current_rate
    assert status == 0.24477


@freeze_time("2021-08-14 13:20:00")
def test_get_rate_data_weekend(test_rates, plandata_mock):
    """Test rate schedules."""
    test_rates.update()
    status = test_rates.current_rate
    assert status == 0.06118


@freeze_time("2021-08-14 13:20:00")
def test_get_rate_data_weekend_demand(test_rates, demand_plandata_mock):
    """Test rate schedules."""
    test_rates.update()
    status = test_rates.current_demand_rate
    assert status == 0


@freeze_time("2021-08-13 10:21:34")
def test_get_rate_data_demand(test_rates, demand_plandata_mock):
    """Test rate schedules."""
    test_rates.update()
    status = test_rates.current_demand_rate
    assert status == 0


@freeze_time("2021-08-13 17:20:00")
def test_get_rate_data_2_demand(test_rates, demand_plandata_mock):
    """Test rate schedules."""
    test_rates.update()
    status = test_rates.current_demand_rate
    assert status == 8.4


def test_get_demand_unit(test_rates, demand_plandata_mock):
    """Test rate schedules."""
    test_rates.update()
    status = test_rates.demand_unit
    assert status == "kW"


def test_get_distributed_generation(test_rates, plandata_mock):
    """Test rate schedules."""
    test_rates.update()
    status = test_rates.distributed_generation
    assert status == "Net Metering"


def test_get_aproval(test_rates, plandata_mock):
    """Test rate schedules."""
    test_rates.update()
    status = test_rates.approval
    assert status


def test_get_name(test_rates, plandata_mock):
    """Test rate schedules."""
    test_rates.update()
    status = test_rates.rate_name
    assert status == "Residential Service TOU Time Advantage 7PM-Noon (ET-2)"


def test_get_lookup_data_404(test_lookup, lookup_mock_404):
    """Test lookup error 404"""
    with pytest.raises(openeihttp.UrlNotFound):
        test_lookup.lookup_plans()


def test_get_lookup_data_401(test_lookup, lookup_mock_401):
    """Test lookup error 401"""
    with pytest.raises(openeihttp.NotAuthorized):
        test_lookup.lookup_plans()


def test_get_plan_data_404(test_rates, plandata_mock_404):
    """Test rate schedules."""
    with pytest.raises(openeihttp.UrlNotFound):
        test_rates.update()


def test_get_plan_data_401(test_rates, plandata_mock_401):
    """Test rate schedules."""
    with pytest.raises(openeihttp.NotAuthorized):
        test_rates.update()


def test_get_plan_data_api_err(test_rates, plandata_mock_api_err, caplog):
    """Test rate schedules."""
    with pytest.raises(openeihttp.APIError):
        test_rates.update()
        assert (
            "No api_key was supplied. Get one at https://api.openei.org:443"
            in caplog.text
        )


def test_get_lookup_data_api_err(test_lookup, lookup_mock_api_err, caplog):
    """Test rate schedules."""
    with pytest.raises(openeihttp.APIError):
        test_lookup.lookup_plans()
        assert (
            "No api_key was supplied. Get one at https://api.openei.org:443"
            in caplog.text
        )


def test_get_all_rates(test_rates, plandata_mock):
    """Test rate schedules."""
    test_rates.update()
    status = test_rates.all_rates
    assert status == [0.24477, 0.06118, 0.19847, 0.06116]


def test_get_all_rates_demand(test_rates, demand_plandata_mock):
    """Test rate schedules."""
    test_rates.update()
    status = test_rates.all_rates
    assert status == [0.07798, 0.11017, 0.1316]


def test_get_lookup_data_radius(test_lookup_radius, lookup_mock_radius, caplog):
    """Test v4 Status reply"""
    status = test_lookup_radius.lookup_plans()
    assert status == {
        "Arizona Public Service Co": [
            {"name": "Time Advantage 7pm to noon", "label": "539fba68ec4f024bc1dc2db3"},
            {
                "name": "Residential Bundled & Adjustments No Tax TOU; Time Adv Super peak 7PM-Noon (ET-SP)",
                "label": "542aec8a5257a310694b1ab6",
            },
            {
                "name": "Residential Service Bundled Standard rate",
                "label": "55563ddf5457a3bf6c8b4570",
            },
            {
                "name": "Residential Bundled & Adjustments No Tax TOU ; Time Adv 7PM-Noon  (ET-2)",
                "label": "55563df55457a35e758b4568",
            },
            {
                "name": "Residential Bundled & Adjustments No Tax TOU w/ Demand; Combined Adv  7PM-Noon (ECT-2)",
                "label": "562bea025457a31838418740",
            },
            {
                "name": "Residential Service Bundled Standard rate",
                "label": "5743aa135457a3a636906f5b",
            },
            {
                "name": "Residential Service TOU Time Advantage 7PM-Noon (ET-2)",
                "label": "574613aa5457a3557e906f5b",
            },
            {
                "name": "Residential Service TOU Combined Advantage 7PM-Noon  (ECT-2)",
                "label": "574615f85457a3557e906f5c",
            },
            {
                "name": "Residential Service Standard (E-12)",
                "label": "5748ab725457a37e7d906f5b",
            },
            {
                "name": "Residential Service TOU Time Advantage 7PM-Noon (ET-2)",
                "label": "5748ac7a5457a37d7d906f5b",
            },
            {
                "name": "Residential Service Standard (E-12)",
                "label": "5881345e5457a35973316ce7",
            },
            {
                "name": "Residential Service TOU Time Advantage 7PM-Noon (ET-2)",
                "label": "588135ee5457a3873f316ce6",
            },
            {
                "name": "Residential Service TOU Combined Advantage 7PM-Noon  (ECT-2)",
                "label": "5890c92f5457a36c373dbec0",
            },
            {
                "name": "Residential Service Standard (E-12) Low Income",
                "label": "59fcde8e5457a3a04cc05084",
            },
            {
                "name": "Residential Service Standard (E-12) [Frozen]",
                "label": "5a592dee5457a3931d423a81",
            },
            {
                "name": "Residential Service TOU Time Advantage 7PM-Noon (ET-2) [Frozen]",
                "label": "5a5930055457a36274423a7d",
            },
            {
                "name": "Residential Service TOU Combined Advantage 7PM-Noon  (ECT-2) [Frozen]",
                "label": "5a5930bf5457a3371c423a7e",
            },
            {
                "name": "Residential Time of Use (Saver Choice)",
                "label": "5a5933d25457a3ad69423a81",
            },
            {
                "name": "Residential Service (Saver Choice Plus)",
                "label": "5a5935475457a3ad69423a82",
            },
            {
                "name": "Residential Service (Saver Choice Max)",
                "label": "5a5936ef5457a36274423a7f",
            },
            {
                "name": "Extra Small Residential Service (Lite Choice)",
                "label": "5a5937bb5457a3b71c423a7f",
            },
            {
                "name": "Small Residential Service (Premier Choice)",
                "label": "5a59388c5457a3931d423a84",
            },
            {
                "name": "Large Residential Service (Premier Choice Large)",
                "label": "5a5939515457a3371c423a7f",
            },
            {
                "name": "Residential Service (Pilot Technology Rate)",
                "label": "5a593d815457a3371c423a80",
            },
            {
                "name": "Extra Small Residential Service (Lite Choice) R-XS",
                "label": "5cacc5605457a379257780e2",
            },
            {
                "name": "Small Residential Service (Premier Choice) R-Basic",
                "label": "5cacc6545457a3634c7780e2",
            },
            {
                "name": "Large Residential Service (Premier Choice Large) R-Basic L [Frozen]",
                "label": "5cacc6e75457a3a8497780e2",
            },
            {
                "name": "Residential Time of Use (Saver Choice) TOU-E",
                "label": "5cacc7715457a393487780e2",
            },
            {
                "name": "Residential Service (Saver Choice Max)",
                "label": "5cacc9ae5457a3c6517780e2",
            },
            {
                "name": "Residential Service (Saver Choice Plus) R-2",
                "label": "5cacc9d15457a31d537780e2",
            },
            {
                "name": "Residential Service (Saver Choice Max) R-3",
                "label": "5caccb2f5457a3c8517780e2",
            },
            {
                "name": "Residential Service (Pilot Technology Rate) R-Tech",
                "label": "5caccd925457a31a537780e2",
            },
        ],
        "Buckeye Water C&D District": [
            {"label": "539fb6fcec4f024bc1dc0679", "name": "Residential"},
            {"label": "539fc06bec4f024c27d89c25", "name": "Private Irrigation Pump"},
        ],
        "Salt River Project": [
            {
                "label": "539f755cec4f024411ed1357",
                "name": "E-23 STANDARD PRICE PLAN FOR RESIDENTIAL " "SERVICE",
            },
            {
                "label": "539fb6a4ec4f024bc1dc028f",
                "name": "E-24 M-POWER PRICE PLAN FOR PRE-PAY " "RESIDENTIAL SERVICE",
            },
            {
                "label": "539fb86aec4f024bc1dc1713",
                "name": "E-21 PRICE PLAN FOR RESIDENTIAL SUPER PEAK "
                "TIME-OF-USE SERVICE",
            },
            {
                "label": "539fbec8ec4f024c27d88a91",
                "name": "E-25 - Experimental Plan for Residential "
                "Super Peak Time-of-Use Service",
            },
            {
                "label": "539fc8d1ec4f024d2f53eab0",
                "name": "E-22 - EXPERIMENTAL PLAN FOR RESIDENTIAL "
                "SUPER PEAK TIME-OF-USE SERVICE",
            },
            {
                "label": "539fc9d6ec4f024d2f53f55c",
                "name": "E-28 M-POWER PRICE PLAN FOR RESIDENTIAL "
                "PRE-PAY TIME-OF-USE SERVICE",
            },
            {
                "label": "539fca4dec4f024d2f53fa1e",
                "name": "E-26 STANDARD PRICE PLAN FOR RESIDENTIAL "
                "TIME-OF-USE SERVICE",
            },
            {
                "label": "548a03535357a3ff32f0c30b",
                "name": "E-22 - EXPERIMENTAL PLAN FOR RESIDENTIAL "
                "SUPER PEAK TIME-OF-USE SERVICE",
            },
            {
                "label": "56c77d785457a3410cb338bb",
                "name": "E-23 BASIC PRICE PLAN FOR RESIDENTIAL " "SERVICE",
            },
            {
                "label": "56c77e775457a3fe28b338bb",
                "name": "E-26 STANDARD PRICE PLAN FOR RESIDENTIAL "
                "TIME-OF-USE SERVICE",
            },
            {
                "label": "56c780355457a30a29b338bb",
                "name": "E-24 M-POWER PRICE PLAN FOR PRE-PAY " "RESIDENTIAL SERVICE",
            },
            {
                "label": "56c781055457a3672db338bb",
                "name": "E-21 PRICE PLAN FOR RESIDENTIAL SUPER PEAK "
                "TIME-OF-USE SERVICE",
            },
            {
                "label": "56c781af5457a35833b338bc",
                "name": "E-22 - EXPERIMENTAL PLAN FOR RESIDENTIAL "
                "SUPER PEAK TIME-OF-USE SERVICE",
            },
            {
                "label": "56c7827e5457a3143ab338bb",
                "name": "E-25 - Experimental Plan for Residential "
                "Super Peak Time-of-Use Service",
            },
            {
                "label": "56c783fe5457a35833b338bd",
                "name": "E-28 M-POWER PRICE PLAN FOR RESIDENTIAL "
                "PRE-PAY TIME-OF-USE SERVICE",
            },
            {
                "label": "5880efe95457a35b73316ce6",
                "name": "E-23 BASIC PRICE PLAN FOR RESIDENTIAL " "SERVICE",
            },
            {
                "label": "5880f0db5457a3c97b316ce6",
                "name": "E-24 M-POWER PRICE PLAN FOR PRE-PAY " "RESIDENTIAL SERVICE",
            },
            {
                "label": "5880f1885457a3e863316ce6",
                "name": "E-26 STANDARD PRICE PLAN FOR RESIDENTIAL "
                "TIME-OF-USE SERVICE",
            },
            {
                "label": "5880f24d5457a33d48316ce6",
                "name": "E-21 PRICE PLAN FOR RESIDENTIAL SUPER PEAK "
                "TIME-OF-USE SERVICE",
            },
            {
                "label": "5880ff0c5457a3d70e316ce6",
                "name": "E-22 - EXPERIMENTAL PLAN FOR RESIDENTIAL "
                "SUPER PEAK TIME-OF-USE SERVICE",
            },
            {
                "label": "5881012e5457a30f3e316ce6",
                "name": "E-25 - Experimental Plan for Residential "
                "Super Peak Time-of-Use Service",
            },
            {
                "label": "588103e85457a3d70e316ce7",
                "name": "E-27 P Pilot Price Plan for Residential "
                "Demand Rate Service",
            },
            {
                "label": "5881042b5457a35b73316ce7",
                "name": "E-28 M-POWER PRICE PLAN FOR RESIDENTIAL "
                "PRE-PAY TIME-OF-USE SERVICE",
            },
            {
                "label": "59f8cac65457a32644c05083",
                "name": "E-23 BASIC PRICE PLAN FOR RESIDENTIAL "
                "SERVICE Low Income Rate",
            },
            {
                "label": "5a55224a5457a3ac5d423a7d",
                "name": "E-23 BASIC PRICE PLAN FOR RESIDENTIAL " "SERVICE",
            },
            {
                "label": "5a58f7fa5457a3ff19423a7c",
                "name": "E-21 PRICE PLAN FOR RESIDENTIAL SUPER PEAK "
                "TIME-OF-USE SERVICE",
            },
            {
                "label": "5a58f8ec5457a3931d423a7c",
                "name": "E-22 - EXPERIMENTAL PLAN FOR RESIDENTIAL "
                "SUPER PEAK TIME-OF-USE SERVICE",
            },
            {
                "label": "5a58f9605457a30e35423a7c",
                "name": "E-24 M-POWER PRICE PLAN FOR PRE-PAY " "RESIDENTIAL SERVICE",
            },
            {
                "label": "5a58f9cd5457a34151423a7c",
                "name": "E-25 - Experimental Plan for Residential "
                "Super Peak Time-of-Use Service",
            },
            {
                "label": "5a58fa865457a3ec1b423a7c",
                "name": "E-26 STANDARD PRICE PLAN FOR RESIDENTIAL "
                "TIME-OF-USE SERVICE",
            },
            {
                "label": "5a58fb8e5457a3b71c423a7c",
                "name": "E-27 P Pilot Price Plan for Residential "
                "Demand Rate Service",
            },
            {
                "label": "5a58fc915457a3ff19423a7d",
                "name": "E-28 M-POWER PRICE PLAN FOR RESIDENTIAL "
                "PRE-PAY TIME-OF-USE SERVICE",
            },
            {
                "label": "5a59008c5457a3ad69423a7c",
                "name": "E-29 EXPERIMENTAL PRICE PLAN FOR TIME-OF-USE "
                "SERVICE WITH SUPER OFF PEAK FOR ELECTRIC "
                "VEHICLES",
            },
            {
                "label": "5cf58ee05457a3160d26c07e",
                "name": "E-23 BASIC PRICE PLAN FOR RESIDENTIAL " "SERVICE",
            },
            {
                "label": "5cf815b25457a3be3326c07d",
                "name": "E-21 PRICE PLAN FOR RESIDENTIAL SUPER PEAK "
                "TIME-OF-USE SERVICE",
            },
            {
                "label": "5cf816af5457a35b2e26c07e",
                "name": "E-22 - EXPERIMENTAL PLAN FOR RESIDENTIAL "
                "SUPER PEAK TIME-OF-USE SERVICE",
            },
            {
                "label": "5cf8174b5457a3562a26c07d",
                "name": "E-24 M-POWER PRICE PLAN FOR PRE-PAY " "RESIDENTIAL SERVICE",
            },
            {
                "label": "5cf817db5457a32f3126c07d",
                "name": "E-25 - Experimental Plan for Residential "
                "Super Peak Time-of-Use Service",
            },
            {
                "label": "5cf8264e5457a3063126c07d",
                "name": "E-26 STANDARD PRICE PLAN FOR RESIDENTIAL "
                "TIME-OF-USE SERVICE",
            },
            {
                "label": "5cf826d55457a3063126c07e",
                "name": "E-27 P Pilot Price Plan for Residential "
                "Demand Rate Service",
            },
            {
                "label": "5cf82a395457a3d92b26c07d",
                "name": "E-29 EXPERIMENTAL PRICE PLAN FOR TIME-OF-USE "
                "SERVICE WITH SUPER OFF PEAK FOR ELECTRIC "
                "VEHICLES",
            },
            {
                "label": "5cf831715457a3612f26c07d",
                "name": "E-28 M-POWER PRICE PLAN FOR RESIDENTIAL "
                "PRE-PAY TIME-OF-USE SERVICE",
            },
            {
                "label": "5d9b7fc95457a3d865598dce",
                "name": "E-14 RESIDENTIAL CUSTOMER GENERATION "
                "ELECTRIC VEHICLE EXPORT PRICE PLAN",
            },
            {
                "label": "5dc498485457a37b0cf6a951",
                "name": "E-13 CUSTOMER GENERATION TIME-OF-USE EXPORT "
                "PRICE PLAN FOR RESIDENTIAL SERVICE",
            },
            {
                "label": "5dc49b5f5457a39661f6a951",
                "name": "E-15 CUSTOMER GENERATION AVERAGE DEMAND "
                "PRICE PLAN FOR RESIDENTIAL SERVICE",
            },
        ],
        "Not Listed": [{"label": "Not Listed", "name": "Not Listed"}],
    }
    # assert "&api_key=[REDACTED]" in caplog.text
    # assert "&lat=[REDACTED]&lon=[REDACTED]" in caplog.text


@freeze_time("2021-08-13 10:21:34")
def test_get_tier_rate_data_low(test_lookup_tier_low, tier_plandata_mock):
    """Test rate schedules."""
    test_lookup_tier_low.update()
    status = test_lookup_tier_low.current_rate
    assert status == 0.25902


@freeze_time("2021-08-13 10:21:34")
def test_get_tier_rate_data_med(test_lookup_tier_med, tier_plandata_mock):
    """Test rate schedules."""
    test_lookup_tier_med.update()
    status = test_lookup_tier_med.current_rate
    assert status == 0.32596


@freeze_time("2021-08-13 10:21:34")
def test_get_tier_rate_data_high(test_lookup_tier_high, tier_plandata_mock):
    """Test rate schedules."""
    test_lookup_tier_high.update()
    status = test_lookup_tier_high.current_rate
    assert status == 0.40745


@freeze_time("2021-08-13 13:20:00")
def test_get_tier_rate_data_2(test_lookup_tier_low, tier_plandata_mock):
    """Test rate schedules."""
    test_lookup_tier_low.update()
    status = test_lookup_tier_low.current_rate
    assert status == 0.25902


@freeze_time("2021-08-14 13:20:00")
def test_get_tier_rate_data_weekend(test_lookup_tier_low, tier_plandata_mock):
    """Test rate schedules."""
    test_lookup_tier_low.update()
    status = test_lookup_tier_low.current_rate
    assert status == 0.25902


@freeze_time("2021-08-13 10:21:34")
def test_get_monthly_tier_rate_data_low(
    test_lookup_monthly_tier_low, tier_plandata_mock
):
    """Test rate schedules."""
    test_lookup_monthly_tier_low.update()
    status = test_lookup_monthly_tier_low.monthly_tier_rate
    assert status == 0.25902


@freeze_time("2021-08-13 10:21:34")
def test_get_monthly_tier_rate_data_med(
    test_lookup_monthly_tier_med, tier_plandata_mock
):
    """Test rate schedules."""
    test_lookup_monthly_tier_med.update()
    status = test_lookup_monthly_tier_med.monthly_tier_rate
    assert status == 0.32596


@freeze_time("2021-08-13 10:21:34")
def test_get_monthly_tier_rate_data_high(
    test_lookup_monthly_tier_high, tier_plandata_mock
):
    """Test rate schedules."""
    test_lookup_monthly_tier_high.update()
    status = test_lookup_monthly_tier_high.monthly_tier_rate
    assert status == 0.40745


def test_get_lookup_data_with_address(test_lookup_address, lookup_mock_address):
    """Test v4 Status reply"""
    status = test_lookup_address.lookup_plans()
    assert status == {
        "Arizona Public Service Co": [
            {"name": "Time Advantage 7pm to noon", "label": "539fba68ec4f024bc1dc2db3"},
            {
                "name": "Residential Bundled & Adjustments No Tax TOU; Time Adv Super peak 7PM-Noon (ET-SP)",
                "label": "542aec8a5257a310694b1ab6",
            },
            {
                "name": "Residential Service Bundled Standard rate",
                "label": "55563ddf5457a3bf6c8b4570",
            },
            {
                "name": "Residential Bundled & Adjustments No Tax TOU ; Time Adv 7PM-Noon  (ET-2)",
                "label": "55563df55457a35e758b4568",
            },
            {
                "name": "Residential Bundled & Adjustments No Tax TOU w/ Demand; Combined Adv  7PM-Noon (ECT-2)",
                "label": "562bea025457a31838418740",
            },
            {
                "name": "Residential Service Bundled Standard rate",
                "label": "5743aa135457a3a636906f5b",
            },
            {
                "name": "Residential Service TOU Time Advantage 7PM-Noon (ET-2)",
                "label": "574613aa5457a3557e906f5b",
            },
            {
                "name": "Residential Service TOU Combined Advantage 7PM-Noon  (ECT-2)",
                "label": "574615f85457a3557e906f5c",
            },
            {
                "name": "Residential Service Standard (E-12)",
                "label": "5748ab725457a37e7d906f5b",
            },
            {
                "name": "Residential Service TOU Time Advantage 7PM-Noon (ET-2)",
                "label": "5748ac7a5457a37d7d906f5b",
            },
            {
                "name": "Residential Service Standard (E-12)",
                "label": "5881345e5457a35973316ce7",
            },
            {
                "name": "Residential Service TOU Time Advantage 7PM-Noon (ET-2)",
                "label": "588135ee5457a3873f316ce6",
            },
            {
                "name": "Residential Service TOU Combined Advantage 7PM-Noon  (ECT-2)",
                "label": "5890c92f5457a36c373dbec0",
            },
            {
                "name": "Residential Service Standard (E-12) Low Income",
                "label": "59fcde8e5457a3a04cc05084",
            },
            {
                "name": "Residential Service Standard (E-12) [Frozen]",
                "label": "5a592dee5457a3931d423a81",
            },
            {
                "name": "Residential Service TOU Time Advantage 7PM-Noon (ET-2) [Frozen]",
                "label": "5a5930055457a36274423a7d",
            },
            {
                "name": "Residential Service TOU Combined Advantage 7PM-Noon  (ECT-2) [Frozen]",
                "label": "5a5930bf5457a3371c423a7e",
            },
            {
                "name": "Residential Time of Use (Saver Choice)",
                "label": "5a5933d25457a3ad69423a81",
            },
            {
                "name": "Residential Service (Saver Choice Plus)",
                "label": "5a5935475457a3ad69423a82",
            },
            {
                "name": "Residential Service (Saver Choice Max)",
                "label": "5a5936ef5457a36274423a7f",
            },
            {
                "name": "Extra Small Residential Service (Lite Choice)",
                "label": "5a5937bb5457a3b71c423a7f",
            },
            {
                "name": "Small Residential Service (Premier Choice)",
                "label": "5a59388c5457a3931d423a84",
            },
            {
                "name": "Large Residential Service (Premier Choice Large)",
                "label": "5a5939515457a3371c423a7f",
            },
            {
                "name": "Residential Service (Pilot Technology Rate)",
                "label": "5a593d815457a3371c423a80",
            },
            {
                "name": "Extra Small Residential Service (Lite Choice) R-XS",
                "label": "5cacc5605457a379257780e2",
            },
            {
                "name": "Small Residential Service (Premier Choice) R-Basic",
                "label": "5cacc6545457a3634c7780e2",
            },
            {
                "name": "Large Residential Service (Premier Choice Large) R-Basic L [Frozen]",
                "label": "5cacc6e75457a3a8497780e2",
            },
            {
                "name": "Residential Time of Use (Saver Choice) TOU-E",
                "label": "5cacc7715457a393487780e2",
            },
            {
                "name": "Residential Service (Saver Choice Max)",
                "label": "5cacc9ae5457a3c6517780e2",
            },
            {
                "name": "Residential Service (Saver Choice Plus) R-2",
                "label": "5cacc9d15457a31d537780e2",
            },
            {
                "name": "Residential Service (Saver Choice Max) R-3",
                "label": "5caccb2f5457a3c8517780e2",
            },
            {
                "name": "Residential Service (Pilot Technology Rate) R-Tech",
                "label": "5caccd925457a31a537780e2",
            },
        ],
        "Not Listed": [{"label": "Not Listed", "name": "Not Listed"}],
    }


@freeze_time("2021-08-13 10:21:34")
def test_get_rate_data_address(test_rates_address, plandata_mock_address):
    """Test rate schedules."""
    test_rates_address.update()
    status = test_rates_address.current_rate
    assert status == 0.06118


def test_missing_loc(test_lookup_missing_loc, caplog):
    """Missing API key check."""
    with pytest.raises(InvalidCall):
        test_lookup_missing_loc.lookup_plans()
        assert "Missing location data for a plan lookup." in caplog.text


def test_mincharge(test_lookup_tier_low, tier_plandata_mock):
    """Test rate schedules."""
    test_lookup_tier_low.update()
    status = test_lookup_tier_low.mincharge
    assert status == (10, "$/month")


def test_mincharge_none(test_rates, plandata_mock):
    """Test rate schedules."""
    test_rates.update()
    status = test_rates.mincharge
    assert status is None

def test_get_rate_data_cache(test_rates, plandata_mock, caplog):
    """Test rate schedules."""
    with caplog.at_level(logging.DEBUG):
        test_rates.update()
    assert "No data populated, refreshing data." in caplog.text
    thefuture = datetime.date.today() + datetime.timedelta(days=3)
    with freeze_time(thefuture):
        with caplog.at_level(logging.DEBUG):
            test_rates.update()    
    assert "Data stale, refreshing from API." in caplog.text