import traceback
from gc import DEBUG_STATS

from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from starlette import status

# 教学模式保持开启
DEBUG_MODE = True

async def http_exception_handler(request: Request, ext: HTTPException):
    """
    处理HTTP异常
    :param request:
    :param ext:
    :return:
    """
    # HTTP异常通常是主动抛出，data保持NONE
    return JSONResponse(
        status_code = ext.status_code,
        content={
            "code": ext.status_code,
            "message": ext.detail,
            "data": None
        }
    )

async def integrity_error_handler(request: Request, exc: IntegrityError):
    """
    处理数据库完整性错误
    :param request:
    :param ext:
    :return:
    """
    error_msg = str(exc.orig)
    if "username_UNIQUE" in error_msg or "Duplicate entry" in error_msg:
        detail = "用户已存在"
    elif "FOREIGN KEY" in error_msg:
        detail = "数据关联错误"
    else:
        detail = "数据约束冲突，请检查输入"

    error_data = None
    if DEBUG_MODE:
        error_data = {
            "error_type": "IntegrityError",
            "error_msg": error_msg,
            "error_path": str(request.url)
        }
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "code": 400,
            "message": detail,
            "data": error_data
        }
    )

async def sqlalchemy_error_handler(request: Request, exc: SQLAlchemyError):
    """
    处理sql错误
    :param request:
    :param ext:
    :return:
    """
    error_data = None
    if DEBUG_MODE:
        error_data={
            "error_type": type(exc).__name__,
            "error_detail": str(exc),
            "traceback": traceback.format_exc(), # 格式化异常信息为字符串
            "path": str(request.url)
        }

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "code": 500,
            "message": "数据库操作失败，请稍后再试",
            "data": error_data
        }
    )


async def general_exception_handler(request: Request, exc:Exception):
    """
    处理其他异常
    :param request:
    :param exc:
    :return:
    """
    # 开发模式下返回详细异常信息
    error_data = None
    if DEBUG_MODE:
        error_data = {
            "error_type": type(exc).__name__,
            "error_detail": str(exc),
            "traceback": traceback.format_exc(),
            "path": str(request.url)
        }
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "code": 500,
            "message": "服务器错误，请稍后再试",
            "data": error_data
        }
    )