import json
import uuid
import graphene
from datetime import datetime


class User(graphene.ObjectType):
    id = graphene.ID(default_value=str(uuid.uuid4()))
    username = graphene.String()
    created_at = graphene.DateTime(default_value=datetime.now())


class Query(graphene.ObjectType):
    hello = graphene.String()
    users = graphene.List(User, limit=graphene.Int())
    is_admin = graphene.Boolean()

    def resolve_hello(self, info):
        return 'world'

    def resolve_is_admin(self, info):
        return True

    def resolve_users(self, info, limit=None):
        return [
            User(id="1", username="Tom", created_at=datetime.now()),
            User(id="2", username="John", created_at=datetime.now()),
        ][:limit]


class CreateUser(graphene.Mutation):
    user = graphene.Field(User)

    class Arguments:
        username = graphene.String()

    def mutate(self, info, username):
        user = User(id="3", username=username, created_at=datetime.now())
        return CreateUser(user=user)


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)

result = schema.execute(
    '''
    {
        users(limit: 1) {
            id
            username
            createdAt
        }
    }
    '''
)

print(result)
# dictResult = dict(result.data.items())
# print(json.dumps(dictResult, indent=2))
