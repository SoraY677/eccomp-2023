#
# ログ出力ラッパー関数
#
import logging
import os
import sys
import datetime

LOG_NAME = "main"
FORMAT = "[%(filename)s:%(lineno)d]\t%(levelname)s\t%(asctime)s\t %(message)s"

_logger = None
_log_func = {}

def init(dirpath=None, level=logging.DEBUG):
    """初期化

    Args:
        filepath (string, optional): ファイルの絶対パス. Defaults to None.
        level (string, optional): ログレベル. Defaults to logging.DEBUG.
    """
    _logger = logging.getLogger("main")
    if dirpath is None:
        handler = logging.StreamHandler()
    else:
        filepath = os.path.join(dirpath, datetime.datetime.now().strftime('%Y%m%d%H%M%S') + ".log")
        handler = logging.FileHandler(filepath)
    handler.setLevel(level)
    handler.setFormatter(logging.Formatter(FORMAT))
    _logger.addHandler(handler)
    
    global _log_func
    _log_func = {
        logging.DEBUG: _logger.debug,
        logging.INFO: _logger.info,
        logging.WARN: _logger.warning,
        logging.ERROR: _logger.error
    }

def _common(text, level):
    """ログ出力用共通関数

    Args:
        text (string): ログ出力テキスト
        level (string): ログレベル 
    """
    func = _log_func[level]
    if func is None:
        sys.exit(1)
    func(text)

def debug(text):
    """debug出力

    Args:
        text (string): ログ出力テキスト
    """
    _common(text, logging.DEBUG)

def info(text):
    """info出力

    Args:
        text (string): ログ出力テキスト
    """
    _common(text, logging.INFO)

def warn(text):
    """warn出力

    Args:
        text (string): ログ出力テキスト
    """
    _common(text, logging.WARN)

def error(text):
    """error出力

    Args:
        text (string): ログ出力テキスト
    """
    _common(text, logging.ERROR)

# 
# 単体テスト
#
if __name__ == "__main__":
    import unittest
    class Test(unittest.TestCase):
        def test_debug(self):
            """debug表示
            """
            text = 'debugテストだよ～'
            init()
            with self.assertLogs(logger=_logger, level=logging.DEBUG) as cm:
                debug(text)
                self.assertEqual(cm.output, [
                    f'DEBUG:{LOG_NAME}:{text}'
                ])

        def test_info(self):
            """info表示
            """
            text = 'infoテストだよ～'
            init()
            with self.assertLogs(logger=_logger, level=logging.INFO) as cm:
                info(text)
                self.assertEqual(cm.output, [
                    f'INFO:{LOG_NAME}:{text}'
                ])

        def test_warn(self):
            """warn表示
            """
            text = 'warnテストだよ～'
            init()
            with self.assertLogs(logger=_logger, level=logging.WARN) as cm:
                warn(text)
                self.assertEqual(cm.output, [
                    f'WARNING:{LOG_NAME}:{text}'
                ])

        def test_error(self):
            """error表示
            """
            text = 'errorまでテストだよ～'
            init()
            with self.assertLogs(logger=_logger, level=logging.ERROR) as cm:
                error(text)
                self.assertEqual(cm.output, [
                    f'ERROR:{LOG_NAME}:{text}'
                ])

        def test_level_select_miss(self):
            """レベル違いでinfoのみ表示
            """
            text = 'レベルの違いでdebug非表示だよ～'
            init()
            with self.assertLogs(logger=_logger, level=logging.INFO) as cm:
                debug(text)
                info(text)
                self.assertEqual(cm.output, [f'INFO:{LOG_NAME}:{text}'])
                pass

        def test_all(self):
            """全ログ表示
            """
            text = '全部のテストだよ～'
            init()
            with self.assertLogs(logger=_logger, level=logging.DEBUG) as cm:
                debug(text)
                info(text)
                warn(text)
                error(text)
                self.assertEqual(cm.output, [
                    f'DEBUG:{LOG_NAME}:{text}',
                    f'INFO:{LOG_NAME}:{text}',
                    f'WARNING:{LOG_NAME}:{text}',
                    f'ERROR:{LOG_NAME}:{text}'
                ])
                
        def test_file_output(self):
            """ファイル存在確認
            """
            import os
            text = 'ファイル出力テストだよ～'
            filepath = '../data/app-log'
            init(filepath)
            debug(text)
            info(text)
            warn(text)
            error(text)
            self.assertTrue(os.path.isfile(filepath))

    unittest.main()