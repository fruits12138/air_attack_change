# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['alien_invasion.py','alien.py','bullet.py','button.py','game_stats.py','scoreboard.py','settings.py','ship.py'],
             pathex=["C:\\Users\\zht\\Desktop\\python_file\\alien_invasion\\alien_invasion.py"],
             binaries=[],
             datas=[('images\\*.bmp', 'images')],
             hiddenimports=['time','sys','pygame','pygame.sprite','pygame.font'],
             hookspath=[],
             hooksconfig={},
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
          a.binaries,
          a.zipfiles,
          a.datas,  
          [],
          icon = 'C:\\Users\\zht\\Desktop\\alien.ico',
          name='alien_invasion',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None )
