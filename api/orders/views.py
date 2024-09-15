from flask_restx import Namespace, Resource, fields
from ..models.orders import Order
from ..models.users import User
from http import HTTPStatus
from flask_jwt_extended import jwt_required
order_namespace=Namespace(
    'orders', description="a namespace for authentication"
)


order_model = order_namespace.model('Order',
     {
        'id': fields.Integer(description='an ID'),
        'size': fields.String(description="Size of order", required=True, enum=['SMALL', 'MEDIUM', 'LARGE', 'EXTRA_LARGE']),
        'order_status': fields.String(description="the status of the order", required=True, enum=['PENDING', 'IN_TRANSIT', 'DELIVERED'])
    })



@order_namespace.route('/')
class HelloOrders(Resource):
    def get(self):
        return {"message": "hello orders"}
    


@order_namespace.route('/orders')
class OrderGetCreate(Resource):

    @order_namespace.marshal_with(order_model) #serialize response
    @jwt_required() #auth needed
    def get(self):
        """ Get all orders"""

        orders = Order.query.all()
        return orders, HTTPStatus.OK
        pass

    def post(self):
        """ Create a new order"""
        pass


@order_namespace.route('/order/<int:order_id>')
class OrderGetCreate(Resource):
    def get(self, order_id):
        """ 
            Retrieve an order by id
        """
        pass

    def put(self, order_id):
        """ 
            Update an order by id
        """
        pass

    def delete(self, order_id):
        """ 
            Delete an order by id
        """
        pass

@order_namespace.route('/user/<int:user_id>/order/<int:order_id>')
class GetSpecificOrderByUser(Resource):
    @jwt_required
    def get(self, user_id, order_id):
        """ Get a users specific order"""
        user = User.get_by_id(user_id)
        order = Order.query.filter_by(id=order_id).filter_by(user=user).first() #this should have been the reverse way
        return order, HTTPStatus.OK


@order_namespace.route('/order/<int:order_id>')
class GetUpdateDelete(Resource):
    @jwt_required()
    def get(self, order_id):
        """
            Retrieve an order by its id
        """
        order = Order.get_by_id(order_id)
        return order, HTTPStatus.OK
    
@order_namespace.route('/user/<int:user_id>/orders')
class UserOrders(Resource):
    @order_namespace.marshal_list_with(order_model)
    @jwt_required()
    def get(self, user_id):
        """
            Get all orders by a specific user
        """

        user = User.get_by_id(user_id)
        orders = user.orders
        return orders, HTTPStatus.OK
