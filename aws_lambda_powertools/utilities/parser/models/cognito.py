from typing import Any, Literal, Optional

from pydantic import BaseModel


# Common context model for Cognito triggers
class CognitoCallerContextModel(BaseModel):
    awsSdkVersion: str
    clientId: str


# Base model for all Cognito triggers
class CognitoTriggerBaseSchema(BaseModel):
    version: str
    region: str
    userPoolId: str
    userName: Optional[str] = None
    callerContext: CognitoCallerContextModel


# Models for Pre-Signup flow
class CognitoPreSignupRequestModel(BaseModel):
    userAttributes: dict[str, Any]
    validationData: Optional[dict[str, Any]] = None
    clientMetadata: Optional[dict[str, Any]] = None
    userNotFound: Optional[bool] = None


class CognitoPreSignupResponseModel(BaseModel):
    autoConfirmUser: Optional[bool] = False
    autoVerifyPhone: Optional[bool] = False
    autoVerifyEmail: Optional[bool] = False


class CognitoPreSignupTriggerModel(CognitoTriggerBaseSchema):
    triggerSource: Literal["PreSignUp_SignUp"]
    request: CognitoPreSignupRequestModel
    response: CognitoPreSignupResponseModel


# Models for Post-Confirmation flow
class CognitoPostConfirmationRequestModel(BaseModel):
    userAttributes: dict[str, Any]
    clientMetadata: Optional[dict[str, Any]] = None


class CognitoPostConfirmationTriggerModel(CognitoTriggerBaseSchema):
    triggerSource: Literal["PostConfirmation_ConfirmSignUp"]
    request: CognitoPostConfirmationRequestModel
    response: dict[str, Any] = {}


# Models for Pre-Authentication flow
class CognitoPreAuthenticationRequestModel(BaseModel):
    userAttributes: dict[str, Any]
    validationData: Optional[dict[str, Any]] = None
    userNotFound: Optional[bool] = None


class CognitoPreAuthenticationTriggerModel(CognitoTriggerBaseSchema):
    triggerSource: Literal["PreAuthentication_Authentication"]
    request: CognitoPreAuthenticationRequestModel
    response: dict[str, Any] = {}


# Models for Post-Authentication flow
class CognitoPostAuthenticationRequestModel(BaseModel):
    userAttributes: dict[str, Any]
    newDeviceUsed: Optional[bool] = None
    clientMetadata: Optional[dict[str, Any]] = None


class CognitoPostAuthenticationTriggerModel(CognitoTriggerBaseSchema):
    triggerSource: Literal["PostAuthentication_Authentication"]
    request: CognitoPostAuthenticationRequestModel
    response: dict[str, Any] = {}


# Models for Pre-Token Generation flow
class CognitoGroupConfigurationModel(BaseModel):
    groupsToOverride: list[str]
    iamRolesToOverride: list[str]
    preferredRole: Optional[str] = None


class CognitoPreTokenGenerationRequestModel(BaseModel):
    userAttributes: dict[str, Any]
    groupConfiguration: CognitoGroupConfigurationModel
    clientMetadata: Optional[dict[str, Any]] = None


class CognitoPreTokenGenerationTriggerModelV1(CognitoTriggerBaseSchema):
    triggerSource: str
    request: CognitoPreTokenGenerationRequestModel
    response: dict[str, Any] = {}


class CognitoPreTokenGenerationRequestModelV2AndV3(CognitoPreTokenGenerationRequestModel):
    scopes: Optional[dict[str, Any]] = None


class CognitoPreTokenGenerationTriggerModelV2AndV3(CognitoTriggerBaseSchema):
    request: CognitoPreTokenGenerationRequestModelV2AndV3
    response: dict[str, Any] = {}


# Models for User Migration flow
class CognitoMigrateUserRequestModel(BaseModel):
    password: str
    validationData: Optional[dict[str, Any]] = None
    clientMetadata: Optional[dict[str, Any]] = None


class CognitoMigrateUserResponseModel(BaseModel):
    userAttributes: Optional[dict[str, Any]] = None
    finalUserStatus: Optional[str] = None
    messageAction: Optional[str] = None
    desiredDeliveryMediums: Optional[list[str]] = None
    forceAliasCreation: Optional[bool] = None
    enableSMSMFA: Optional[bool] = None


class CognitoMigrateUserTriggerModel(CognitoTriggerBaseSchema):
    triggerSource: str
    userName: str
    request: CognitoMigrateUserRequestModel
    response: CognitoMigrateUserResponseModel


# Models for Custom Message flow
class CognitoCustomMessageRequestModel(BaseModel):
    userAttributes: dict[str, Any]
    codeParameter: str
    linkParameter: Optional[str] = None
    usernameParameter: Optional[str] = None
    clientMetadata: Optional[dict[str, Any]] = None


class CognitoCustomMessageResponseModel(BaseModel):
    smsMessage: Optional[str] = None
    emailMessage: Optional[str] = None
    emailSubject: Optional[str] = None


class CognitoCustomMessageTriggerModel(CognitoTriggerBaseSchema):
    triggerSource: str
    request: CognitoCustomMessageRequestModel
    response: CognitoCustomMessageResponseModel


# Models for Custom Email/SMS Sender flow
class CognitoCustomEmailSMSSenderRequestModel(BaseModel):
    type: str
    code: str
    clientMetadata: Optional[dict[str, Any]] = None
    userAttributes: dict[str, Any]


class CognitoCustomEmailSenderTriggerModel(CognitoTriggerBaseSchema):
    triggerSource: Literal["CustomEmailSender_SignUp"]
    request: CognitoCustomEmailSMSSenderRequestModel


class CognitoCustomSMSSenderTriggerModel(CognitoTriggerBaseSchema):
    triggerSource: Literal["CustomSMSSender_SignUp"]
    request: CognitoCustomEmailSMSSenderRequestModel


# Models for Challenge Authentication flows
class CognitoChallengeResultModel(BaseModel):
    challengeName: Literal[
        "SRP_A",
        "PASSWORD_VERIFIER",
        "SMS_MFA",
        "EMAIL_OTP",
        "SOFTWARE_TOKEN_MFA",
        "DEVICE_SRP_AUTH",
        "DEVICE_PASSWORD_VERIFIER",
        "ADMIN_NO_SRP_AUTH",
    ]
    challengeResult: bool
    challengeMetadata: Optional[str] = None


class CognitoAuthChallengeRequestModel(BaseModel):
    userAttributes: dict[str, Any]
    session: list[CognitoChallengeResultModel]
    clientMetadata: Optional[dict[str, Any]] = None
    userNotFound: Optional[bool] = None


class CognitoDefineAuthChallengeResponseModel(BaseModel):
    challengeName: Optional[str] = None
    issueTokens: Optional[bool] = None
    failAuthentication: Optional[bool] = None


class CognitoDefineAuthChallengeTriggerModel(CognitoTriggerBaseSchema):
    triggerSource: Literal["DefineAuthChallenge_Authentication"]
    request: CognitoAuthChallengeRequestModel
    response: CognitoDefineAuthChallengeResponseModel


class CognitoCreateAuthChallengeResponseModel(BaseModel):
    publicChallengeParameters: Optional[dict[str, Any]] = None
    privateChallengeParameters: Optional[dict[str, Any]] = None
    challengeMetadata: Optional[str] = None


class CognitoCreateAuthChallengeTriggerModel(CognitoTriggerBaseSchema):
    triggerSource: Literal["CreateAuthChallenge_Authentication"]
    request: CognitoAuthChallengeRequestModel
    response: CognitoCreateAuthChallengeResponseModel


class CognitoVerifyAuthChallengeRequestModel(BaseModel):
    userAttributes: dict[str, Any]
    privateChallengeParameters: dict[str, Any]
    challengeAnswer: str
    clientMetadata: Optional[dict[str, Any]] = None
    userNotFound: Optional[bool] = None


class CognitoVerifyAuthChallengeResponseModel(BaseModel):
    answerCorrect: bool


class CognitoVerifyAuthChallengeTriggerModel(CognitoTriggerBaseSchema):
    triggerSource: Literal["VerifyAuthChallengeResponse_Authentication"]
    request: CognitoVerifyAuthChallengeRequestModel
    response: CognitoVerifyAuthChallengeResponseModel
