import functools

# from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.csrf import csrf_exempt
# from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

import json
import httplib as http

from modularodm import Q

import utils

from framework.auth.core import User as OsfUser
from framework.mongo.utils import get_or_http_error
from framework.exceptions import HTTPError
from website.project.model import MetaSchema, DraftRegistration
from website.exceptions import NodeStateError

get_draft_or_error = functools.partial(get_or_http_error, DraftRegistration)

# use update to directly insert into db

# def get_prereg_users():
#     """Retrieves users on the admin site who are in the prereg_group
#     :return: List of usernames of those who are in the prereg_group
#     """
#     reviewers = []
#     users = User.objects.all()
#     for reviewer in users:
#         if (is_in_prereg_group(reviewer)):
#             reviewers.append(str(reviewer.username))
#     return reviewers

def is_in_prereg_group(user):
    """Determines whether a user is in the prereg_group
    :param user: User wanting access to prereg material
    :return: True if prereg False if not
    """
    return user.groups.filter(name='prereg_group').exists()

# @login_required
# @user_passes_test(is_in_prereg_group)
def prereg(request):
    """Redirects to prereg page if user has prereg access
    :param request: Current logged in user
    :return: Redirect to prereg page with username, reviewers, and user obj
    """
    #prereg_admin = request.user.has_perm('auth.prereg_admin')
    #user = {
    #     'username': str(request.user.username),
    #     'admin': json.dumps(prereg_admin)
    # }
    user = {
        'username': 'user_placeholder',
        'admin': 'admin_placeholder'
    }
    #reviewers = get_prereg_users()
    reviewers = ['admin_placeholder']

    #context = {'user_info': user, 'reviewers': reviewers, 'user': request.user}
    context = {
        'user_info': user,
        'reviewers': reviewers
    }
    return render(request, 'pre-reg/prereg.html', context)

# @login_required
# @user_passes_test(is_in_prereg_group)
def prereg_form(request, draft_pk):
    """Redirects to prereg form review page if user has prereg access
    :param draft_pk: Unique id for selected draft
    :return: Redirect to prereg form review page with draft obj
    """
    draft = get_draft_or_error(draft_pk)
    context = {
        'draft': utils.serialize_draft_registration(draft)
    }
    return render(request, 'pre-reg/edit_draft_registration.html', context)

# @login_required
# @user_passes_test(is_in_prereg_group)
def get_drafts(request):
    """Determines whether a user is in the general_administrator_group
    :param user: User wanting access to administrator material
    :return: True if general administrator False if not
    """
    prereg_schema = MetaSchema.find_one(
        Q('name', 'eq', 'Prereg Challenge') &
        Q('schema_version', 'eq', 2)
    )
    all_drafts = DraftRegistration.find(
        Q('registration_schema', 'eq', prereg_schema) &
        Q('approval', 'ne', None)
    )
    serialized_drafts = {
        'drafts': [utils.serialize_draft_registration(d) for d in all_drafts]
    }

    paginator = Paginator(serialized_drafts['drafts'], 15)

    page = request.GET.get('page')
    try:
        drafts = paginator.page(page)
    except PageNotAnInteger:
        drafts = paginator.page(1)
    except EmptyPage:
        drafts = paginator.page(paginator.num_pages)

    return JsonResponse(
        dict(drafts=drafts.object_list)
    )

# @login_required
# @user_passes_test(is_in_prereg_group)
@csrf_exempt
def approve_draft(request, draft_pk):  # TODO
    """Approves current draft
    :param user: Current logged in user
    :param draft_pk: Unique id for current draft
    :return: DraftRegistrationApproval obj
    """
    draft = get_draft_or_error(draft_pk)

    # TODO[lauren]: add proper authorizers to DraftRegistrationApproval
    # params for approve function = self, user, and token
    # user should be the admin
    user = OsfUser.load('dsmpw')
    draftRegistrationApproval = draft.approval

    draftRegistrationApproval.add_authorizer(user)
    token = draftRegistrationApproval.approval_state[user._id]['approval_token']
    draftRegistrationApproval.approve(user, token)
    draftRegistrationApproval.save()

    return JsonResponse({})

# @login_required
# @user_passes_test(is_in_prereg_group)
@csrf_exempt
def reject_draft(request, draft_pk):  # TODO
    """Rejects current draft
    :param user: Current logged in user
    :param draft_pk: Unique id for current draft
    :return: DraftRegistrationApproval obj
    """
    draft = get_draft_or_error(draft_pk)

    # TODO[lauren]: add proper authorizers to DraftRegistrationApproval
    # need to pass self, user, and token
    # user should be the admin
    user = OsfUser.load('dsmpw')
    draftRegistrationApproval = draft[0].approval

    draftRegistrationApproval.add_authorizer(user)
    token = draftRegistrationApproval.approval_state[user._id]['rejection_token']

    draftRegistrationApproval.reject(user, token)
    draftRegistrationApproval.save()

    return JsonResponse({})


# @login_required
# @user_passes_test(is_in_prereg_group)
@csrf_exempt
def update_draft(request, draft_pk):
    """Updates current draft to save admin comments

    :param draft_pk: Unique id for current draft
    :return: DraftRegistration obj
    """
    data = json.load(request)
    draft = get_draft_or_error(draft_pk)

    schema_data = data.get('schema_data', {})
    try:
        draft.update_metadata(schema_data)
        draft.save()
    except (NodeStateError):
        raise HTTPError(http.BAD_REQUEST)
    return JsonResponse(
        {
            'draft': utils.serialize_draft_registration(draft)
        }
    )
