from framework.utils import iso8601format
from website.project.metadata.utils import serialize_meta_schema
from website import settings
from website.filters import gravatar
from website.util.permissions import reduce_permissions

def serialize_user(user, node=None, admin=False, full=False):
    """
    Return a dictionary representation of a registered user.

    :param User user: A User object
    :param bool full: Include complete user properties
    """
    fullname = user.display_full_name(node=node)
    ret = {
        'id': str(user._primary_key),
        'registered': user.is_registered,
        'surname': user.family_name,
        'fullname': fullname,
        'shortname': fullname if len(fullname) < 50 else fullname[:23] + "..." + fullname[-23:],
        'gravatar_url': gravatar(
            user, use_ssl=True,
            size=settings.PROFILE_IMAGE_MEDIUM
        ),
        'active': user.is_active,
    }
    if node is not None:
        if admin:
            flags = {
                'visible': False,
                'permission': 'read',
            }
        else:
            flags = {
                'visible': user._id in node.visible_contributor_ids,
                'permission': reduce_permissions(node.get_permissions(user)),
            }
        ret.update(flags)
    if user.is_registered:
        ret.update({
            'url': user.url,
            'absolute_url': user.absolute_url,
            'display_absolute_url': user.display_absolute_url,
            'date_registered': user.date_registered.strftime("%Y-%m-%d"),
        })

    if full:
        # Add emails
        ret['emails'] = [
            {
                'address': each,
                'primary': each == user.username,
                'confirmed': True,
            } for each in user.emails
        ] + [
            {
                'address': each,
                'primary': each == user.username,
                'confirmed': False
            }
            for each in user.unconfirmed_emails
        ]

        if user.is_merged:
            merger = user.merged_by
            merged_by = {
                'id': str(merger._primary_key),
                'url': merger.url,
                'absolute_url': merger.absolute_url
            }
        else:
            merged_by = None
        ret.update({
            'is_merged': user.is_merged,
            'merged_by': merged_by,
        })

    return ret


# TODO: Write and use APIv2 serializer for this
def serialize_draft_registration(draft):

    return {
        'pk': draft._id,
        'initiator': serialize_user(draft.initiator, full=True),
        'registration_metadata': draft.registration_metadata,
        'registration_schema': serialize_meta_schema(draft.registration_schema),
        'initiated': iso8601format(draft.datetime_initiated),
        'updated': iso8601format(draft.datetime_updated),
        'flags': draft.flags,
        'requires_approval': draft.requires_approval,
        'is_pending_approval': draft.is_pending_review,
        'is_approved': draft.is_approved,
        'notes': draft.notes
    }
