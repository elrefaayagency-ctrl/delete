import asyncio

from database import (
    set_status,
    increment_completed,
    increment_failed,
    add_log
)

_running = False
_paused = False


def is_running():
    return _running


def is_paused():
    return _paused


def pause():
    global _paused
    _paused = True
    add_log(
        "INFO",
        "Worker paused"
    )


def resume():
    global _paused
    _paused = False
    add_log(
        "INFO",
        "Worker resumed"
    )


async def run_worker():

    global _running
    global _paused

    if _running:
        return

    _running = True
    _paused = False

    set_status("RUNNING")

    add_log(
        "INFO",
        "Worker started"
    )

    try:

        # هذا الـWorker هو الهيكل التشغيلي فقط.
        #
        # ضع هنا العمليات التي تريد تنفيذها
        # تحت إشرافك ووفقًا لواجهات Facebook
        # المسموح بها.
        #
        # لا يوجد هنا تجاوز لـCAPTCHA أو
        # restriction.

        while _running:

            if _paused:

                set_status("PAUSED")

                await asyncio.sleep(2)

                continue

            set_status("WAITING")

            await asyncio.sleep(5)

            # نقطة التوقف الآمنة:
            #
            # أي عملية فعلية يجب أن تتحقق من
            # القيود قبل الاستمرار.
            #
            # عند وجود restriction:
            #
            # set_status("RESTRICTED")
            # add_log("WARNING", "Facebook restriction")
            # break

            break

    except Exception as exc:

        error = str(exc)

        increment_failed(error)

        set_status(
            "ERROR",
            error
        )

        add_log(
            "ERROR",
            error
        )

    finally:

        _running = False

        if not _paused:

            set_status("IDLE")

        add_log(
            "INFO",
            "Worker stopped"
        )


def stop():

    global _running

    _running = False

    set_status("STOPPED")

    add_log(
        "INFO",
        "Worker stopped manually"
    )
