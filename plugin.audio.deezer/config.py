config = {
    'parameters': {
        'plugin.name': 'plugin.audio.deezer',
        'plugin.env': 'dev',
        'app.settings.path': 'resources\settings.xml'
    },

    'services': {
        'app.settings': {
            'class': 'Services:Settings',
            'arguments': ["@app.settings.path"]
        }
    },

    'routing': {
        'list_settings': {
            'path': '/settings',
            'defaults': {
                '_controller': 'Controllers:Settings:list'
            }
        },

        'show_setting': {
            'path': '/settings/<id>',
            'defaults': {
                '_controller': 'Controllers:Settings:show'
            }
        }
    }
}

#config = {'service_container': {}, 'router': {'rules': [{'regex': '^\\/(?P<user>[^/]+?)$', 'module': 'resources.lib.app.settings', 'target': 'Settings:show_settings', 'rule': '/<user>'}, {'regex': '^\\/$', 'module': 'resources.lib.app.settings', 'target': 'Settings:show_settings', 'rule': '/'}]}, 'plugin': {'name': 'plugin.audio.deezer', 'env': 'dev'}}