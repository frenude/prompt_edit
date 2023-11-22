import time
from typing import Optional, Callable


class TimeReport:
    """一个计时上下文管理器, 提供代码执行计时功能
    例如:
        >>> with TimeReport():
        >>>    time.sleep(2)
        Timer 执行用时: 2.0051秒 (2005.124毫秒)

        >>> with TimeReport(silence=True) as t:
        >>>     time.sleep(2)
        >>> print(t.total_seconds)
        2.003908157348633
    """

    def __init__(
            self,
            name: str = "Timer",
            output_func: Optional[Callable] = print,
            disable: bool = False,
            extra_msg: Optional[str] = None,
            silence: bool = False,
    ):
        self._name = name
        self.start_time = None
        self.output_func = output_func
        self.extra_msg = extra_msg
        self.disable = disable
        self.total_seconds = 0
        self.silence = silence
        self.report_str = ""

    def current_exec_seconds(self):
        if self.disable:
            return 0
        return time.time() - self.start_time

    def __enter__(self):
        if self.disable:
            return self
        self.start_time = time.time()
        return self

    def __exit__(self, *args):
        if self.disable:
            return
        self.total_seconds = time.time() - self.start_time
        if self.total_seconds > 3600:
            hours = self.total_seconds // 3600
            remaining_seconds = self.total_seconds % 3600
            minutes = remaining_seconds // 60
            remaining_seconds = remaining_seconds % 60
            self.report_str += f"{hours}时{minutes}分{remaining_seconds:.2f}秒"
        elif self.total_seconds > 60:
            minutes = self.total_seconds // 60
            remaining_seconds = self.total_seconds % 60
            self.report_str += f"{minutes}分{remaining_seconds:.3f}秒"
        else:
            self.report_str += (
                f"{self.total_seconds:.4f}秒 ({self.total_seconds * 1000:.3f}毫秒)"
            )
        if self.extra_msg:
            self.report_str = f"{self.report_str}, {self.extra_msg}"
        if self.output_func and not self.silence:
            self.output_func(f"{self._name} 执行用时: " + self.report_str)
