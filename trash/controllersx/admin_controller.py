from flask import Blueprint, request, jsonify
from models import db, Merchant

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin/merchants', methods=['GET'])
def get_all_merchants():
    merchants = Merchant.query.all()
    return jsonify([merchant.to_dict() for merchant in merchants])

@admin_bp.route('/admin/merchants/<int:id>/verify', methods=['PUT'])
def verify_merchant(id):
    merchant = Merchant.query.get_or_404(id)
    merchant.verified = True
    db.session.commit()
    return jsonify({'message': 'Merchant verified successfully'}), 200

@admin_bp.route('/admin/merchants/<int:id>/suspend', methods=['PUT'])
def suspend_merchant(id):
    merchant = Merchant.query.get_or_404(id)
    merchant.suspended = True
    db.session.commit()
    return jsonify({'message': 'Merchant suspended successfully'}), 200