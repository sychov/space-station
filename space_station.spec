# -*- mode: python -*-

block_cipher = None

added_files = [
         ( './gamedata/*.*', 'gamedata' ),
         ( './gamedata/map/*.*', 'gamedata/map' ),
         ( './gamedata/text/objects/*.*', 'gamedata/text/objects' ),
         ( './graphics/chars/*.*', 'graphics/chars' ),
         ( './graphics/interface/*.*', 'graphics/interface' ),
         ( './graphics/tilesets/*.*', 'graphics/tilesets' ),
         ( './sounds/music/*.*', 'sounds/music' ),
         ( './sounds/sound/*.*', 'sounds/sound' ),
         ]

a = Analysis(['./source/main.py'],
             pathex=['./build'],
             binaries=[],
             datas=added_files,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
			 
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
			 
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='space_station',
          debug=False,
          strip=False,
          upx=True,
          console=True)
		  
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='space_station')
