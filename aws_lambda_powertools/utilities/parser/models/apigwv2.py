from datetime import datetime
from typing import Any, Literal, Optional, Union

from pydantic import BaseModel, Field, field_validator
from pydantic.networks import IPvAnyNetwork

from aws_lambda_powertools.utilities.parser.functions import _validate_source_ip


class RequestContextV2AuthorizerIamCognito(BaseModel):
    amr: list[str]
    identityId: str
    identityPoolId: str


class RequestContextV2AuthorizerIam(BaseModel):
    accessKey: Optional[str] = None
    accountId: Optional[str] = None
    callerId: Optional[str] = None
    principalOrgId: Optional[str] = None
    userArn: Optional[str] = None
    userId: Optional[str] = None
    cognitoIdentity: Optional[RequestContextV2AuthorizerIamCognito] = None


class RequestContextV2AuthorizerJwt(BaseModel):
    claims: dict[str, Any]
    scopes: Optional[list[str]] = None


class RequestContextV2Authorizer(BaseModel):
    jwt: Optional[RequestContextV2AuthorizerJwt] = None
    iam: Optional[RequestContextV2AuthorizerIam] = None
    lambda_value: Optional[dict[str, Any]] = Field(None, alias="lambda")


class RequestContextV2Http(BaseModel):
    method: Literal["DELETE", "GET", "HEAD", "OPTIONS", "PATCH", "POST", "PUT"]
    path: str
    protocol: str
    sourceIp: Union[IPvAnyNetwork, str]
    userAgent: str

    @field_validator("sourceIp", mode="before")
    @classmethod
    def _validate_source_ip(cls, value):
        return _validate_source_ip(value=value)


class RequestContextV2(BaseModel):
    accountId: str
    apiId: str
    authorizer: Optional[RequestContextV2Authorizer] = None
    domainName: str
    domainPrefix: str
    requestId: str
    routeKey: str
    stage: str
    time: str
    timeEpoch: datetime
    http: RequestContextV2Http


class APIGatewayProxyEventV2Model(BaseModel):
    version: str
    routeKey: str
    rawPath: str
    rawQueryString: str
    cookies: Optional[list[str]] = None
    headers: dict[str, str]
    queryStringParameters: Optional[dict[str, str]] = None
    pathParameters: Optional[dict[str, str]] = None
    stageVariables: Optional[dict[str, str]] = None
    requestContext: RequestContextV2
    body: Optional[Union[str, type[BaseModel]]] = None
    isBase64Encoded: Optional[bool] = None


class ApiGatewayAuthorizerRequestV2(APIGatewayProxyEventV2Model):
    type: Literal["REQUEST"]
    routeArn: str
    identitySource: Optional[list[str]] = None
