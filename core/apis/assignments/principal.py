from flask import Blueprint
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment, AssignmentStateEnum
from core.models.teachers import Teacher
from .schema import AssignmentSchema, AssignmentGradeSchema

principal_assignments_resources = Blueprint('principal_assignments_resources', __name__)

@principal_assignments_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_submitted_graded_assignments(p):
    """Returns list of submitted and graded assignments"""
    submitted_graded_assignments = Assignment.query.filter(
        Assignment.state.in_([AssignmentStateEnum.SUBMITTED, AssignmentStateEnum.GRADED])
    ).all()
    assignments_dump = AssignmentSchema().dump(submitted_graded_assignments, many=True)
    return APIResponse.respond(data=assignments_dump)

@principal_assignments_resources.route('/teachers', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_teachers(p):
    """Returns list of all teachers"""
    teachers = Teacher.query.all()
    teachers_dump = [teacher.to_dict() for teacher in teachers]
    return APIResponse.respond(data=teachers_dump)

@principal_assignments_resources.route('/assignments/grade', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal
def grade_assignment(p, incoming_payload):
    """Grade or re-grade an assignment"""
    grade_assignment_payload = AssignmentGradeSchema().load(incoming_payload)
    assignment = Assignment.query.get(grade_assignment_payload.id)

    assignment.grade = grade_assignment_payload.grade
    assignment.state = AssignmentStateEnum.GRADED
    db.session.commit()

    assignment_dump = AssignmentSchema().dump(assignment)
    return APIResponse.respond(data=assignment_dump)
