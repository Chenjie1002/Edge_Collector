from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from app.services.deployment_plc import (
    DeploymentConfigUnavailable,
    activate_candidate,
    load_active_deployment_config,
    load_candidate,
    load_line_options,
    rollback_activation,
    save_candidate,
    test_connection,
    validate_candidate,
)


router = APIRouter(prefix="/api/v2/deployment/plc", tags=["deployment"])


@router.get("/active")
def active_configuration() -> dict[str, object]:
    try:
        return load_active_deployment_config()
    except DeploymentConfigUnavailable as exc:
        raise HTTPException(status_code=503, detail="Active PLC configuration is not available.") from exc


@router.get("/line-options")
def line_options() -> dict[str, object]:
    try:
        return load_line_options()
    except DeploymentConfigUnavailable as exc:
        raise HTTPException(status_code=503, detail="Line configuration options are not available.") from exc


@router.post("/validate", response_model=None)
def validate(payload: dict[str, Any]) -> dict[str, object] | JSONResponse:
    try:
        result = validate_candidate(payload)
    except DeploymentConfigUnavailable as exc:
        raise HTTPException(status_code=503, detail="PLC deployment configuration is not available.") from exc
    if result.get("errors"):
        return JSONResponse(status_code=422, content=result)
    return result


@router.post("/test-connection", response_model=None)
def connection_test(payload: dict[str, Any]) -> dict[str, object] | JSONResponse:
    try:
        result = test_connection(payload)
    except DeploymentConfigUnavailable as exc:
        raise HTTPException(status_code=503, detail="PLC deployment configuration is not available.") from exc
    if result["status"] == "INVALID_CONFIGURATION":
        return JSONResponse(status_code=422, content=result)
    return result


@router.post("/candidates", response_model=None)
def create_candidate(payload: dict[str, Any]) -> dict[str, object] | JSONResponse:
    try:
        result = save_candidate(payload)
    except DeploymentConfigUnavailable as exc:
        raise HTTPException(status_code=503, detail="PLC deployment configuration is not available.") from exc
    if result.get("errors"):
        return JSONResponse(status_code=422, content=result)
    return result


@router.post("/candidates/{candidate_id}/activate", response_model=None)
def activate(candidate_id: str) -> dict[str, object] | JSONResponse:
    try:
        result = activate_candidate(candidate_id)
    except DeploymentConfigUnavailable as exc:
        raise HTTPException(status_code=503, detail="PLC activation could not be completed safely.") from exc
    if result.get("status") != "ACTIVATED_RESTART_REQUIRED":
        return JSONResponse(status_code=409, content=result)
    return result


@router.post("/activations/{activation_id}/rollback", response_model=None)
def rollback(activation_id: str) -> dict[str, object] | JSONResponse:
    try:
        result = rollback_activation(activation_id)
    except DeploymentConfigUnavailable as exc:
        raise HTTPException(status_code=503, detail="PLC activation rollback is not available.") from exc
    if result.get("status") != "ROLLED_BACK":
        return JSONResponse(status_code=409, content=result)
    return result


@router.get("/candidates/{candidate_id}")
def get_candidate(candidate_id: str) -> dict[str, object]:
    try:
        return load_candidate(candidate_id)
    except DeploymentConfigUnavailable as exc:
        raise HTTPException(status_code=404, detail="Candidate configuration is not available.") from exc
