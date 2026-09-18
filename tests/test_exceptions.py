import pytest

from konnektr_graph.exceptions import (
    AuthenticationError,
    HttpResponseError,
    KonnektrGraphError,
    ResourceExistsError,
    ResourceNotFoundError,
    ServiceUnavailableError,
    ValidationError,
)


class TestKonnektrGraphError:
    def test_base_error(self):
        err = KonnektrGraphError("something went wrong", 500)
        assert str(err) == "something went wrong"
        assert err.status_code == 500

    def test_base_error_no_status(self):
        err = KonnektrGraphError("generic error")
        assert err.status_code is None


class TestHttpResponseError:
    def test_inheritance(self):
        assert issubclass(HttpResponseError, KonnektrGraphError)

    def test_creation(self):
        err = HttpResponseError("bad request", 400)
        assert err.status_code == 400


class TestResourceNotFoundError:
    def test_inheritance(self):
        assert issubclass(ResourceNotFoundError, HttpResponseError)

    def test_creation(self):
        err = ResourceNotFoundError("not found", 404)
        assert err.status_code == 404


class TestResourceExistsError:
    def test_inheritance(self):
        assert issubclass(ResourceExistsError, HttpResponseError)

    def test_creation(self):
        err = ResourceExistsError("conflict", 409)
        assert err.status_code == 409


class TestAuthenticationError:
    def test_inheritance(self):
        assert issubclass(AuthenticationError, HttpResponseError)

    def test_creation(self):
        err = AuthenticationError("unauthorized", 401)
        assert err.status_code == 401


class TestValidationError:
    def test_inheritance(self):
        assert issubclass(ValidationError, KonnektrGraphError)

    def test_creation(self):
        err = ValidationError("invalid input")
        assert err.status_code is None


class TestServiceUnavailableError:
    def test_inheritance(self):
        assert issubclass(ServiceUnavailableError, HttpResponseError)

    def test_creation(self):
        err = ServiceUnavailableError("pgvector is not installed", 503)
        assert err.status_code == 503
