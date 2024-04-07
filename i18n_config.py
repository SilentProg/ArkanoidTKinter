import i18n

from game_frame import Settings
i18n.set('locale', Settings().getLanguage()['code'])
i18n.set('filename_format', '{locale}.{format}')
i18n.set('file_format', 'json')
i18n.load_path.append('locales')
