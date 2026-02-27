"""Unit tests for interaction filtering logic."""

from app.models.interaction import InteractionLog
from app.routers.interactions import _filter_by_item_id


def _make_log(id: int, learner_id: int, item_id: int) -> InteractionLog:
    return InteractionLog(id=id, learner_id=learner_id, item_id=item_id, kind="attempt")


def test_filter_returns_all_when_item_id_is_none() -> None:
    interactions = [_make_log(1, 1, 1), _make_log(2, 2, 2)]
    result = _filter_by_item_id(interactions, None)
    assert result == interactions


def test_filter_returns_empty_for_empty_input() -> None:
    result = _filter_by_item_id([], 1)
    assert result == []


def test_filter_returns_interaction_with_matching_ids() -> None:
    interactions = [_make_log(1, 1, 1), _make_log(2, 2, 2)]
    result = _filter_by_item_id(interactions, 1)
    assert len(result) == 1
    assert result[0].id == 1

def test_filter_excludes_interaction_with_different_learner_id() -> None:
    interactions = [_make_log(1, 2, 1)]
    result = _filter_by_item_id(interactions, 1)
    assert len(result) == 1
    assert result[0].id == 1
    assert result[0].learner_id == 2
    assert result[0].item_id == 1


def test_filter_returns_multiple_matches_for_same_item_id() -> None:
    interactions = [
        _make_log(1, 1, 5),
        _make_log(2, 2, 5),
        _make_log(3, 3, 5),
        _make_log(4, 1, 10),
    ]
    result = _filter_by_item_id(interactions, 5)
    assert len(result) == 3
    assert all(i.item_id == 5 for i in result)


def test_filter_returns_empty_when_no_match_found() -> None:
    interactions = [_make_log(1, 1, 1), _make_log(2, 2, 2)]
    result = _filter_by_item_id(interactions, 999)
    assert result == []


def test_filter_handles_zero_item_id() -> None:
    interactions = [
        _make_log(1, 1, 0),
        _make_log(2, 2, 1),
        _make_log(3, 3, 0),
    ]
    result = _filter_by_item_id(interactions, 0)
    assert len(result) == 2
    assert all(i.item_id == 0 for i in result)


def test_filter_handles_negative_item_id() -> None:
    interactions = [
        _make_log(1, 1, -1),
        _make_log(2, 2, 1),
        _make_log(3, 3, -1),
    ]
    result = _filter_by_item_id(interactions, -1)
    assert len(result) == 2
    assert all(i.item_id == -1 for i in result)


def test_filter_handles_large_item_id() -> None:
    large_id = 2**31 - 1
    interactions = [
        _make_log(1, 1, large_id),
        _make_log(2, 2, 100),
    ]
    result = _filter_by_item_id(interactions, large_id)
    assert len(result) == 1
    assert result[0].item_id == large_id


def test_filter_returns_multiple_matches() -> None:
    interactions = [_make_log(1, 1, 3), _make_log(2, 2, 3), _make_log(3, 1, 1)]
    result = _filter_by_item_id(interactions, 3)
    assert len(result) == 2


def test_filter_returns_empty_when_no_match() -> None:
    interactions = [_make_log(1, 1, 1), _make_log(2, 2, 2)]
    result = _filter_by_item_id(interactions, 99)
    assert result == []


def test_filter_with_item_id_zero() -> None:
    interactions = [_make_log(1, 1, 0), _make_log(2, 2, 1)]
    result = _filter_by_item_id(interactions, 0)
    assert len(result) == 1
    assert result[0].id == 1
