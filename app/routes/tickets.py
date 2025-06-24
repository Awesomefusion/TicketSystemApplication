from flask import Blueprint, render_template, redirect, url_for, request, flash, abort
from flask_login import login_required, current_user
from .. import db
from ..models import Ticket, User, Comment, Department
from ..forms import TicketForm, CommentForm, UserAdminForm

tickets_bp = Blueprint(
    'tickets',
    __name__,
    url_prefix='/tickets',
    template_folder='../templates/tickets'
)

def is_it_support():
    return getattr(current_user.department, 'name', None) == 'IT Support'

def same_department(user_id):
    ticket_user = User.query.get(user_id)
    return ticket_user is not None and ticket_user.department_id == current_user.department_id

def has_ticket_access(ticket):
    """
    Allow view/comment if admin, IT Support, or same department as creator
    """
    return (
        current_user.role == 'admin'
        or is_it_support()
        or same_department(ticket.created_by)
    )

def _load_assignees(form):
    """
    Admin sees all users; others only themselves
    """
    users = User.query.all() if current_user.role == 'admin' else [current_user]
    form.assigned_to.choices = [(u.id, u.username) for u in users]

@tickets_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role == 'admin' or is_it_support():
        total = Ticket.query.count()
        open_ = Ticket.query.filter_by(status='Open').count()
        in_progress = Ticket.query.filter_by(status='In Progress').count()
        closed = Ticket.query.filter_by(status='Closed').count()
    else:
        total = Ticket.query.filter_by(created_by=current_user.id).count()
        open_ = Ticket.query.filter_by(created_by=current_user.id, status='Open').count()
        in_progress = Ticket.query.filter_by(created_by=current_user.id, status='In Progress').count()
        closed = Ticket.query.filter_by(created_by=current_user.id, status='Closed').count()

    return render_template(
        'dashboard.html',
        total=total,
        open=open_,
        in_progress=in_progress,
        closed=closed
    )

@tickets_bp.route('/')
@login_required
def list_tickets():
    status_filter = request.args.get('status')
    assignee_filter = request.args.get('assignee', type=int)
    page = request.args.get('page', 1, type=int)
    per_page = 10

    query = Ticket.query
    if not (current_user.role == 'admin' or is_it_support()):
        query = query.join(User, Ticket.created_by == User.id) \
                     .filter(User.department_id == current_user.department_id)

    if status_filter:
        query = query.filter_by(status=status_filter)
    if assignee_filter:
        query = query.filter_by(assigned_to=assignee_filter)

    pagination = query.order_by(Ticket.created_at.desc()) \
                      .paginate(page=page, per_page=per_page, error_out=False)
    tickets = pagination.items
    assignees = User.query.all() if current_user.role == 'admin' else []

    return render_template(
        'list.html',
        tickets=tickets,
        pagination=pagination,
        assignees=assignees,
        status_filter=status_filter,
        assignee_filter=assignee_filter
    )

@tickets_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_ticket():
    form = TicketForm()
    _load_assignees(form)
    if form.validate_on_submit():
        ticket = Ticket(
            title=form.title.data,
            description=form.description.data,
            status=form.status.data,
            created_by=current_user.id,
            assigned_to=form.assigned_to.data
        )
        db.session.add(ticket)
        db.session.commit()
        flash('Ticket created', 'success')
        return redirect(url_for('tickets.list_tickets'))
    return render_template('form.html', form=form, action='Create')

@tickets_bp.route('/<int:ticket_id>')
@login_required
def view_ticket(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    if not has_ticket_access(ticket):
        abort(403)
    comment_form = CommentForm()
    return render_template('view.html', ticket=ticket, comment_form=comment_form)

@tickets_bp.route('/<int:ticket_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_ticket(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    # Only admin or IT Support may edit
    if current_user.role != 'admin' and not is_it_support():
        abort(403)

    form = TicketForm(obj=ticket)
    _load_assignees(form)
    if form.validate_on_submit():
        ticket.title = form.title.data
        ticket.description = form.description.data
        ticket.status = form.status.data
        ticket.assigned_to = form.assigned_to.data
        db.session.commit()
        flash('Ticket updated', 'success')
        return redirect(url_for('tickets.view_ticket', ticket_id=ticket.id))
    return render_template('form.html', form=form, action='Edit')

@tickets_bp.route('/<int:ticket_id>/delete', methods=['POST'])
@login_required
def delete_ticket(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    # Only admin or IT Support may delete
    if current_user.role != 'admin' and not is_it_support():
        abort(403)
    db.session.delete(ticket)
    db.session.commit()
    flash('Ticket deleted', 'warning')
    return redirect(url_for('tickets.list_tickets'))

@tickets_bp.route('/<int:ticket_id>/comment', methods=['POST'])
@login_required
def comment_ticket(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    if not has_ticket_access(ticket):
        abort(403)
    form = CommentForm()
    if not form.validate_on_submit():
        abort(400)
    new_comment = Comment(
        ticket_id=ticket.id,
        user_id=current_user.id,
        comment=form.comment.data
    )
    db.session.add(new_comment)
    db.session.commit()
    flash('Comment added', 'success')
    return redirect(url_for('tickets.view_ticket', ticket_id=ticket.id))

@tickets_bp.route('/comment/<int:comment_id>/delete', methods=['POST'])
@login_required
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    # Only admin or IT Support may delete comments
    if current_user.role != 'admin' and not is_it_support():
        abort(403)
    ticket_id = comment.ticket_id
    db.session.delete(comment)
    db.session.commit()
    flash('Comment deleted', 'warning')
    return redirect(url_for('tickets.view_ticket', ticket_id=ticket_id))

@tickets_bp.route('/admin/users', methods=['GET', 'POST'])
@login_required
def manage_users():
    if current_user.role != 'admin':
        abort(403)
    users = User.query.all()
    departments = Department.query.all()
    department_choices = [(d.id, d.name) for d in departments]

    forms = {}
    for user in users:
        form = UserAdminForm(obj=user)
        form.role.data = user.role
        form.department_id.choices = department_choices
        form.department_id.data = user.department_id
        forms[user.id] = form

    if request.method == 'POST':
        user_id = int(request.form['user_id'])
        form = forms[user_id]
        if form.validate_on_submit():
            u = User.query.get(user_id)
            u.role = form.role.data
            u.department_id = form.department_id.data
            db.session.commit()
            flash(f"Updated {u.username}", 'success')
            return redirect(url_for('tickets.manage_users'))

    return render_template('admin_users.html', users=users, forms=forms)
