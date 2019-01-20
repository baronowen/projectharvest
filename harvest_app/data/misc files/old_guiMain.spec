# -*- mode: python -*-

block_cipher = None


a = Analysis(['guiMain.py'],
             pathex=['C:\\Users\\owena\\git\\projectharvest\\harvest_app'],
             binaries=[],
             datas=[],
             hiddenimports=['tkinter', 'harvest_app', 'harvest_app.pages.guiDataLC', 'harvest_app.pages.guiDataManip', 'harvest_app.pages.guiMerging', 'harvest_app.pages.guiCluster', 'harvest_app.pages.guiAdwords'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='guiMain',
          debug=True,
          bootloader_ignore_signals=False,
          strip=False,
          upx=False,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='guiMain')
