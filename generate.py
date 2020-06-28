#!/usr/bin/env python3
# -*- coding: utf8 -*-
import os
import hashlib
from jinja2 import Environment, FileSystemLoader
import yaml
# importing shutil module
import shutil
import hashlib

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


def render(withkey, id, name, shortname, hostname_prefix, seed, port, v4net, v6net, lon, lat, zoom, wifi24channel, htmode24,wifi5channel,htmode5, nextnode4, nextnode6, authorized_keys):
    j2_env = Environment(loader=FileSystemLoader(THIS_DIR),
                         trim_blocks=True)
    return j2_env.get_template('template_site.j2').render(
        withkey=withkey,
        id=id,
        name=name,
        shortname=shortname,
        hostname_prefix=hostname_prefix,
        seed=seed,
        port=port,
        v4net=v4net,
        v6net=v6net,
        fastdpeers=fastdpeers,
        lon=lon,
        lat=lat,
        zoom=zoom,
        wifi24channel=wifi24channel,
        htmode24=htmode24,
        wifi5channel=wifi5channel,
        htmode5=htmode5,
        nextnode4=nextnode4,
        nextnode6=nextnode6,
        authorized_keys=authorized_keys
    )

def copyStatic(ordnername, keyversion = False):
    key = ''
    if keyversion:
        key = '-key'
    shutil.copytree(THIS_DIR + '/static/', THIS_DIR + '/out/' + ordnername + key + '/' , dirs_exist_ok=True)

def renderI18n(templatefile, name_adj):
    j2_env = Environment(loader=FileSystemLoader(THIS_DIR),
                         trim_blocks=True)
    return j2_env.get_template(templatefile + '.j2').render(
        name_adj=name_adj
    )

def copyI18n(ordnername, name_adj, keyversion = False):
    key = ''
    if keyversion:
        key = '-key'
    if not os.path.exists(THIS_DIR + '/out/' + ordnername + key + '/i18n'):
        os.mkdir(THIS_DIR + '/out/' + ordnername + key + '/i18n')
    with open(THIS_DIR + '/out/' + ordnername + key + '/i18n/en.po', 'w') as f:
        f.write(renderI18n('en.po', name_adj))
    with open(THIS_DIR + '/out/' + ordnername + key + '/i18n/de.po', 'w') as f:
        f.write(renderI18n('de.po', name_adj))

if __name__ == '__main__':
    ansible_base = ''
    for ldir in os.listdir('.'):
        if 'ansible-ff' in ldir:
            ansible_base = ldir
    if not ansible_base:
        raise SystemExit('Could not find a ansible Base. ansible-ff.. \nAborting')

    with open(r'{0}/group_vars/all'.format(ansible_base)) as file:
    # The FullLoader parameter handles the conversion from YAML
    # scalar values to Python the dictionary format
        list = yaml.load(file, Loader=yaml.FullLoader)

        try:
            global_admin_list=list['gluon_global_vars']['authorized_admins']
        except KeyError:
            global_admin_list=[]
        try:
            global_wifi24channel=list['gluon_global_vars']['wifi24channel']
        except KeyError:
            global_wifi24channel=1
        try:
            global_wifi5channel=list['gluon_global_vars']['wifi5channel']
        except KeyError:
            global_wifi5channel=44

        for id, values in list['domaenen'].items():
            print("Verarbeite Domaene {}".format(id))
            try:
                name = values['name']
                try:
                    name_adj = values['name_adj']
                except KeyError:
                    name_adj = name.lower() + "er"
                shortname = values['shortname']
                hostname_prefix = values['hostname_prefix']
                #community = values['community']
                #seed = 'ff'+str(43131800000000000000000000000000000000000000000000000000000000+int(id))
                m = hashlib.sha256()
                m.update(name.encode('utf-8'))
                seed = m.hexdigest()
                v4net = values['ffv4_network']
                v6net = values['ffv6_network']
                #fastdpeers = values['fastdpeers']
                port = values.get('port', 20000 + int(id))
                v6prefix = v6net[:-3]
                lon=values['lon']
                lat=values['lat']
                zoom=values['zoom']
                if 'wifi24channel' in values:
                    wifi24channel=values['wifi24channel']
                else:
                    wifi24channel=global_wifi24channel
                try:
                    htmode24=values['htmode24']
                except KeyError:
                    htmode24="HT20"
                if 'wifi5channel' in values:
                    wifi5channel=values['wifi5channel']
                else:
                    wifi5channel=global_wifi5channel
                try:
                    htmode5=values['htmode5']
                except KeyError:
                    htmode5="HT40"
                try:
                    nextnode4=values['nextnode4']
                    nextnode6=values['nextnode6']
                except KeyError:
                    nextnode4=False
                    nextnode6=False
                try:
                    authorized_keys=[]
                    admins=[]
                    admin_list=[]
                    if 'authorized_admins' in values:
                        admin_list.extend(values['authorized_admins'])
                    admin_list.extend(global_admin_list)
                    for admin in admin_list:
                        if admin not in admins:
                            admins.append(admin)
                            fo = open("{0}/keyfiles/{1}.pub".format(ansible_base, admin), "r")
                            authorized_keys.append(fo.read())
                except KeyError:
                    authorized_keys=[
                    ''
                    ]
            except KeyError as err:
                print("Variable {} fehlt in der ansible group_vars/all bei {}".format(err, id))
                print("Setze generation aus.")
                continue

            try:
                fastdpeers = values['fastdpeers']
            except KeyError:
                fastdpeers = False

            if not os.path.exists(THIS_DIR + '/out'):
                os.mkdir(THIS_DIR + '/out')

            ordnername = id + '_' + shortname

            if not os.path.exists(THIS_DIR + '/out/' + ordnername):
                os.mkdir(THIS_DIR + '/out/' + ordnername)
            with open(THIS_DIR + '/out/' + ordnername + '/site.conf', 'w') as f:
                f.write(render(False, int(id), name, shortname, hostname_prefix, seed, port, v4net, v6net, lon, lat, zoom, wifi24channel, htmode24, wifi5channel, htmode5, nextnode4, nextnode6, authorized_keys))
            copyStatic(ordnername)
            copyI18n(ordnername, name_adj)


            if not os.path.exists(THIS_DIR + '/out/' + ordnername + '-key'):
                os.mkdir(THIS_DIR + '/out/' + ordnername + '-key')
            with open(THIS_DIR + '/out/' + ordnername + '-key/site.conf', 'w') as f:
                f.write(render(True, int(id), name, shortname, hostname_prefix, seed, port, v4net, v6net, lon, lat, zoom, wifi24channel, htmode24, wifi5channel, htmode5, nextnode4, nextnode6, authorized_keys))
            copyStatic(ordnername, keyversion = True)
            copyI18n(ordnername, name_adj, keyversion = True)

    # for id, values in domains.items():
    #     names = values['names']
    #     mesh_id = values['mesh_id']
    #
    #     seed = 'ff'+str(48143000000000000000000000000000000000000000000000000000000000+id)
    #     hide = values.get('hide', False)
    #     port = values.get('port', 20000 + id)
    #     full_id = str(id).zfill(2)
    #     if id == 99:
    #         primary_code = 'insel'
    #     else:
    #         primary_code = 'ffmsd' + full_id
    #     hex_id = hex(id).split('x')[-1]
    #     with open(THIS_DIR + '/' + primary_code + '.conf', 'w') as f:
    #         f.write(render(id, names, seed, hide, port, full_id, hex_id, mesh_id))
