from flask import Blueprint, render_template, redirect, url_for, request, flash, abort
from flask_login import login_required, current_user
from .. import db
from ..models import Ticket, User, Comment
from ..forms import TicketForm, CommentForm

tickets_bp = Blueprint(
    'tickets',
    __name__,
    url_prefix='/tickets',
    template_folder='../templates/tickets'
)

def _load_assignees(form):
    users = User.query.all() if current_user.role == 'admin' else [current_user]
    form.assigned_to.choices = [(u.id, u.username) for u in users]

@tickets_bp.route('/')
@login_required
def list_tickets():
    if current_user.role == 'admin':
        tickets = Ticket.query.all()
    else:
        tickets = Ticket.query.filter_by(created_by=current_user.id).all()
    return render_template('list.html', tickets=tickets)

@tickets_bp.route('/create', methods=['GET','POST'])
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
    return render_template('form.html', form=form, action="Create")

@tickets_bp.route('/<int:ticket_id>')
@login_required
def view_ticket(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    if current_user.role!='admin' and ticket.created_by!=current_user.id:
        abort(403)
    comment_form = CommentForm()
    return render_template(
        'view.html',
        ticket=ticket,
        comment_form=comment_form
    )

@tickets_bp.route('/<int:ticket_id>/edit', methods=['GET','POST'])
@login_required
def edit_ticket(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    if current_user.role!='admin' and ticket.created_by!=current_user.id:
        abort(403)
    form = TicketForm(obj=ticket)
    _load_assignees(form)
    if form.validate_on_submit():
        ticket.title       = form.title.data
        ticket.description = form.description.data
        ticket.status      = form.status.data
        ticket.assigned_to = form.assigned_to.data
        db.session.commit()
        flash('Ticket updated', 'success')
        return redirect(
            url_for('tickets.view_ticket', ticket_id=ticket.id)
        )
    return render_template('form.html', form=form, action="Edit")

@tickets_bp.route('/<int:ticket_id>/delete', methods=['POST'])
@login_required
def delete_ticket(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    if current_user.role!='admin':
        abort(403)
    db.session.delete(ticket)
    db.session.commit()
    flash('Ticket deleted', 'warning')
    return redirect(url_for('tickets.list_tickets'))

@tickets_bp.route('/<int:ticket_id>/comment', methods=['POST'])
@login_required
def comment_ticket(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    if current_user.role!='admin' and ticket.created_by!=current_user.id:
        abort(403)
    form = CommentForm()
    if form.validate_on_submit():
        new_comment = Comment(
            ticket_id=ticket.id,
            user_id=current_user.id,
            comment=form.comment.data
        )
        db.session.add(new_comment)
        db.session.commit()
        flash('Comment added', 'success')
    else:
        flash('Failed to post comment', 'error')
    return redirect(url_for('tickets.view_ticket', ticket_id=ticket.id))
