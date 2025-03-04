import pytest
from pydantic import AnyUrl
from pydantic_core import PydanticCustomError

from sempyro.utils.validator_functions import convert_to_mailto, validate_convert_email

@pytest.mark.parametrize("email", ["mailto:exampleemail@domain.com",
                                   "mailto://exampleemail@domain.com",
                                   "exampleemail@domain.com",
                                   "mailto:http://exampleemail@domain.com"
                                   ])
def test_convert_to_mailto(email):
    calculated = convert_to_mailto(email)
    expected = AnyUrl("mailto:exampleemail@domain.com")
    assert calculated == expected


@pytest.mark.parametrize("email", ["my:email@gmail.com",
                                   "myemailgmail.com",
                                   "mailto:emailgmail.com",
                                   "http://email@gmail.com",
                                   ])
def test_email_validation(email):
    with pytest.raises(PydanticCustomError):
        _ = validate_convert_email(email)
