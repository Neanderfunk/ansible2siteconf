#!/usr/bin/env python3
# -*- coding: utf8 -*-
import os
import hashlib
from jinja2 import Environment, FileSystemLoader
import yaml

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


def render(withkey, id, name, shortname, hostname_prefix, seed, v4net, v6net):
    j2_env = Environment(loader=FileSystemLoader(THIS_DIR),
                         trim_blocks=True)
    return j2_env.get_template('template_site.j2').render(
        withkey=withkey,
        id=id,
        name=name,
        shortname=shortname,
        hostname_prefix=hostname_prefix,
        seed=seed,
        v4net=v4net,
        v6net=v6net,
        #fastdpeers=fastdpeers,
        lon=lon,
        lat=lat,
        zoom=zoom,
        wifi24channel=wifi24channel,
        htmode24=htmode24,
        wifi5channel=wifi5channel,
        htmode5=htmode5,
        nextnode4=nextnode4,
        nextnode6=nextnode6




    )

if __name__ == '__main__':


    with open(r'ansible-ffnef/group_vars/all') as file:
    # The FullLoader parameter handles the conversion from YAML
    # scalar values to Python the dictionary format
        list = yaml.load(file, Loader=yaml.FullLoader)

        #print(list['domaenen'])

        for id, values in list['domaenen'].items():
#            print(id)
#            print(values)

            name = values['name']
            shortname = values['shortname']
            hostname_prefix = values['hostname_prefix']
            #community = values['community']
            seed = 'ff'+str(43131800000000000000000000000000000000000000000000000000000000+id)
            v4net = values['ffv4_network']
            v6net = values['ffv6_network']
            #fastdpeers = values['fastdpeers']
            port = values.get('port', 20000 + id)
            v6prefix = v6net[:-3]
            lon=values['lon']
            lat=values['lat']
            zoom=values['zoom']
            wifi24channel=values['wifi24channel']
            htmode24=['htmode24']
            wifi5channel=['wifi5channel']
            htmode5=['htmode5']
            nextnode4=['nextnode4']
            nextnode6=['nextnode6']


            if not os.path.exists(THIS_DIR + '/out'):
                os.mkdir(THIS_DIR + '/out')

            if not os.path.exists(THIS_DIR + '/out/' + shortname):
                os.mkdir(THIS_DIR + '/out/' + shortname)
            with open(THIS_DIR + '/out/' + shortname + '/site.conf', 'w') as f:
                f.write(render(False, id, name, shortname, hostname_prefix, seed, v4net, v6net))

            if not os.path.exists(THIS_DIR + '/out/' + shortname + '-key'):
                os.mkdir(THIS_DIR + '/out/' + shortname + '-key')
            with open(THIS_DIR + '/out/' + shortname + '-key/site.conf', 'w') as f:
                f.write(render(True, id, name, shortname, hostname_prefix, seed, v4net, v6net))

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
