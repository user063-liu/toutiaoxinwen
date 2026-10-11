from fastapi import APIRouter, Query, Depends, HTTPException
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from config.db_conf import get_db
from crud import news


# 模块化路由
router = APIRouter(prefix="/api/news", tags=["news"])


# 获取分类接口
@router.get("/categories")
async def get_categories(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    categories = await news.get_categories(db, skip, limit)
    # 先获取分类数据，再响应返回数据

    return{
        "code": 200,
        "message": "获取分类成功",
        "data": categories,
    }

@router.get("/list")
async def get_news_list(
        category_id: int = Query(..., alias="categoryId"),
        page: int = Query(1, description="页码"),
        page_size: int = Query(10, alias="pageSize", le=100, description="每页数量"),
        db: AsyncSession = Depends(get_db)
):   # 处理分页规则 获取新闻列表 计算总量 计算是否有更多
    offset = (page - 1) * page_size
    news_list = await news.get_news_list(db, category_id, offset, page_size)
    total = await news.get_news_count(db, category_id)
    has_more = (offset+len(news_list)) < total
    return {
        "code": 200,
        "message": "获取新闻列表成功",
        "data": {
            "list": news_list,
            "total": total,
            "hasMore": has_more,
        },
    }


@router.get("/detail")
async def get_news_detail(
        news_id: int=Query(..., alias="id"),
        db: AsyncSession = Depends(get_db)
):
    news_detail = await news.get_news_detail(db, news_id)
    if not news_detail:
        raise HTTPException(status_code=404, detail="News not found")

    increase_res= await news.increase_news_views(db, news_detail.id)
    if not increase_res:
        raise HTTPException(status_code=404, detail="增加浏览量失败")

    related_news = await news.get_related_news(db, news_detail.id, news_detail.category_id, 5)
    return {
        "code": 200,
        "message": "获取新闻详情成功",
        "data": {
            "id": news_detail.id,
            "title": news_detail.title,
            "content": news_detail.content,
            "image": news_detail.image,
            "author": news_detail.author,
            "publish_time": news_detail.publish_time,
            "category_id": news_detail.category_id,
            "views": news_detail.views,
            "relatedNews": related_news
        }
    }


