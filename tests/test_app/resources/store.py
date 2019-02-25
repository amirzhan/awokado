from typing import List

import sqlalchemy as sa
from marshmallow import fields

import tests.test_app.models as m
from awokado import custom_fields
from awokado.consts import CREATE, READ
from awokado.utils import ReadContext
from tests.test_app.resources.base import Resource


class StoreResource(Resource):
    class Meta:
        model = m.Store
        name = "store"
        methods = (CREATE, READ)
        auth = None

    id = fields.Int(model_field=m.Store.id)
    book_ids = custom_fields.NotNullableList(
        fields.Int(), model_field=m.Book.id, allow_none=True
    )
    name = fields.String(model_field=m.Store.name, required=True)

    def read__query(self, ctx):
        q = (
            sa.select(
                [
                    m.Store.id.label("id"),
                    m.Store.name.label("name"),
                    sa.func.array_agg(m.Book.id).label("book_ids"),
                ]
            )
            .select_from(
                sa.outerjoin(m.Store, m.Book, m.Store.id == m.Book.store_id)
            )
            .group_by(m.Store.id)
        )

        if not ctx.is_list:
            q = q.where(m.Store.id == ctx.resource_id)

        ctx.q = q

    def get_by_book_ids(
        self, session, ctx: ReadContext, field: sa.Column = None
    ):
        q = (
            sa.select(
                [
                    m.Store.id.label("id"),
                    m.Store.name.label("name"),
                    sa.func.array_agg(m.Book.id).label("book_ids"),
                ]
            )
            .select_from(
                sa.outerjoin(m.Store, m.Book, m.Store.id == m.Book.store_id)
            )
            .where(m.Book.id.in_(ctx.obj_ids))
            .group_by(m.Store.id)
        )

        result = session.execute(q).fetchall()
        serialized_objs = self.dump(result, many=True)
        return serialized_objs