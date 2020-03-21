import json
import plone.api
from zope.component.hooks import setSite


site = app.inst
setSite(site)


result = dict(
    users=[],
    groups=[])

# Groups 
for group in plone.api.group.get_groups():
    roles = group.getRoles()
    members = plone.api.user.get_users(groupname=group.getId())
    members = [m.getUserName() for m in members]
    result['groups'].append(dict(
        roles=roles,
        id=group.getId(),
        title=group.Title(),
        members=members))


# Users
passwords = site.acl_users.source_users._user_passwords
for d in plone.api.user.get_users():
    user = plone.api.user.get(d.id)
    if not user:
        continue
    pw = passwords.get(d.id)
    username = user.getUserName()
    email = user.getProperty('email')
    roles = user.getRoles()
    fullname = user.getProperty('fullname')
    result['users'].append(dict(
             id=d.id,
             username=username,
             password=pw, 
             fullname=fullname, 
             email=email, 
             roles=roles))

with open('userdata.json', 'wb') as fp:
    json.dump(result, fp, indent=4)


