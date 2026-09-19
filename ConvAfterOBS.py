# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Michiru (@sudo_ai)
# ConvAfterOBS is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, version 3.

import os
import sys
import shutil
import tempfile
import threading
import subprocess
import webbrowser
import tkinter as tk
from tkinter import filedialog, scrolledtext, ttk

SUBPROCESS_FLAGS = subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0

COLOR_GREEN = "#5bb974"
COLOR_GREEN_HOVER = "#48a060"
COLOR_WARNING = "#b33a3a"

DEFAULT_RES_KEY = "1708x1112 (~16:10)"
DEFAULT_FPS_KEY = "24 кадра"

SAMPLE_POSITIONS = (0.25, 0.50, 0.75)
SAMPLE_LEN_SEC = 60
PREVIEW_TRIGGER_SEC = 200

RES = {
    "1708x1112 (~16:10)": (1708, 1112),
    "1920x1080 (16:9)": (1920, 1080)
}

FPS = {
    "24 кадра": 24,
    "60 кадров": 60
}

TG_ICON_DATA = "iVBORw0KGgoAAAANSUhEUgAAABIAAAASCAYAAABWzo5XAAADL0lEQVR4nK1UzWtcVRT/nXPvm4/MJOlMsTWC2iaNECIuShUx4MavinFRhGzEipWAbt1L/wO3XfgFgpsuxIXSFNtNsEixiKBVSMg0/ZgQQ81o+l5m5r17z5F7p5Ngcel5m/vOOb/f+bjnHsJQzp83WFjw4Tj5+dprnJjT4v0cRB6JduYNNuaKFP6L1jtT3z6IoahQZRDJ5LmfpqnW+AjAPFkLzftQiX4gNqBSGepc+P1Gs84HrfePrw6xHFmJ5Oi5X5+hWuMql6vzWvRUupmoOB0mHM5RV/Q0+FC9cTVgAjZwMK5f1+kvb05yrbYEpoZLOw7EBCIGaJDxICdiJrbGUH6v40SpETABGzii49FPf79g682TLt12RGzxgJj7dLtO0XWCw7UEFuKy0rhF1llqvTvzKh35ZOVlU0ouatGXQRbD+IGA4ESRFYJQ40yzjFNTY3jyYBkf/rCF22kulXKVXT9/xTLrItkEWvRjP5jCDRB6XpAVHmMlxouP1fHWzAG88GgNosClWynWd3LULCuMBXN/0arq81L0AjpwxOh9r5g+UMb8ZB1vHBuPmQRZ+ytHs2Lw/cZu9BlNwK7oIXBYYnMI3oOIKPeKZydG8N5TTcxNjKCW7FWKlU4fhSjqpQSXb6fR5hUUsWwO7XvqoCd/7DrcywVVu2/azBzupAVmD1ZwYT1F6+8cFcOxb0NhFb8FY6BQDbdzc6fA4qU2XvrqBpbbGf7sevxyt4cTh6sR8PXaTuxhjAzViBW/xUS0zEkl6EMfUTGEhyoWv2338fbFNpbvpHj64SrGSiZm9uPmLkYSGjgrJGAjhwh9rK7Yey7BHi6biPDcRBU/3+3hzHft2NxrW120M4fyflkUsIHjPwcyKENjp8ZL2Nx1sdxTx8ZC+bh8K8NoycCLd7betC7dXroRBhJnz/L0E2eOiJdr4YlIv7tHlovCEiExhDSXOB9lSxAvjitVC9EOGz6xuvLZOmN2llbffLwlWXYyGGy9YaESPikxaQCH6R6xpGWDoFY72ogkAROwgeN/WyODB3p/FbQWjq8CeD0sNmJ/WonmQBwXmxJtkPgr6uXfi40oRvoHtInEN4izdlgAAAAASUVORK5CYII="

GH_ICON_DATA = "iVBORw0KGgoAAAANSUhEUgAAABIAAAASCAYAAABWzo5XAAACv0lEQVR4nI1US2sUQRCu6u6Z1fg6icJKZJNJWNaYZM1BBCEnb0nIZQ4iiIg3f4B4CgH/guLNg6LIXgRB8GYgHnII0TyWPHY3Go2GiChIjDszXSXV2dnEPMCCXYqq7/u6uqqmAfYaAoQaDrRQcrgP6R9TAEDitBUKrQr8i0DUvpVRVYJoolYur+zG7hIaUQCjdLZQOO2xPwrIV5XSx7ABYWAgsr+A8VmM0cjHcnkt5ewUcuq5zq5uo81L43utSRwDEUcALDmBklLoG8+DJIpXEpsMLi/OTqdc+XPAXFfXKaXNKwbIRvX6U2L6po32EdHIT3yJSU4wghVOWoiCMJSqSFt9z/NMlplmq/PT1zDmC8TJkLK2B5Ok1/kJFiUnGMEKx/UpDNFdraOjJ8uaF5XWh62185j8LlYqlfp+MwuCIMOmZUprnSdrN9Fi59LS+1V3LTJ8GbVukUYw4iMR6evr8yB0o966fhhqiUlOMIIVjnDTJgMy5BQiMzMg23GJTU62EZRKtjFi57uYw9txwQpHuE0hdlpuggysjrul61/fs3TgYqEGUicEzg2upExjRz6AnKAUEvEwQOk1vIF0hbZtbEwqZFDnh1x3WQqC5aYQxjROSAkD/0TEG0G+d6aC7x5uHbhtQRD44LXcBMBbRMQMEGFs30LaxGp17hMzv1CovgPRdaXxfue54o9cvnugKZLvHkD/6ByifsDMqLWWop4LVzQMlEpyKnIEt+EQ1kDhlXoUFTKeP6QTNdHYfiaj1zRDOxHVldYZa+1XTequy5dKbv1lElirTa8TJf2IOOwZcydO4tU/fiQ9caYZNpiIjDYZIP7MTIMLC1NfGge5T0SMZBrV+ZnJzRiKgHDS87zHR6zOpn2S6wDCBpF9wrG9JNjGk9J8AXZaKgzyChQKBX9HozNBcP7MftiDTP3Hw7ZH5C+myVc9YUeWwgAAAABJRU5ErkJggg=="

QR_CODE_DATA = "iVBORw0KGgoAAAANSUhEUgAAAFAAAABQCAAAAACreq1xAAAQJklEQVR42rVZeZxU1ZX+zr33varqvZulu4FGdpqlWQwIY1Ro0YlJ0BATl6j5kZgY/WUcjWaMiRoVRNGoySQ6SZwAipE4cVwAIzpBIooa4wayI9ACAXvf6Kruqvfevd/8UVXdrfHPmftH1bu3zjn3vHO/e7YSghafGEoBiPIzLZZKfZJGKVoYAM59klULhPi/HYbSsM0MXglPneFU8HyfgBTqC4re+HDq3K5NVAMUc6aeeKVose/Uzve9wazRmeOIkKs+tcctDNjRPzvIL+MK7v0Exd3cAN3JgLd8inUVQwPETWxE/s1FmpMFAPT8dlEdHeJiGpP2Dz1y1KDGo4CANPX2HE1OGKYBFJiiSuZZ+XEmDiDkE5iYCtKZTCaTyaTDhbibIV2Q6Y3uFQ/xI0xlfuvHITuCdBAEmXQwBwl/cSbtGPJuLAzznEFqIp5gaABAYrpfawEgEA9WazoAiGkVAEjkzaUQhc7Pk5r+A1ACAAYAGKlv7NdO3LDnCgmLd64pe7bcuUvO2r8UDndsOnvHwct4if7x1zbd4lk5ZJy8Oc9p+9B8CzL11VZFZWufjNgvECI7DgBAiRUA6PogFomHmppKgHhv+9SZ8RA7cERad+a06XobQCsAiH37JACkRTAgEChUygmLcouqKLKr94pr1lrhX+tnByUPMhbVI+5ri2smrH912nes5+qgAEhRUqhcYR6HuW/n4IQ54NOxVK9+GwBSwJe+BFTfmEVgAOC68c1/GXNdv8HhnHDgzuQFiohIlgAAgmfK5o4+vLt8npfA3/7uKVosKKY5ZbEX4eWdvGD0s7F6Az/PChH5lMCAFkSQ0xCppfjzuQ9dN34jHO56AQCwrwI46ywAsz64b8OmL8fb/CjPStg8a7/A6jbtxFXm9xHjTjSmKotPYGhsdLVnhdLR5JAosa2obi6yunpYY2FJFnMjjaKy1YMFCt2zTgCqhMuJtLwOVx16tzb+3uj7V4oQXHTQS39t7bHT0i/O8FT9/o4zOzeebSEu8XqW1XEAhxJDcT88c4eEHrAokcwQufPrOAn0gt1hogTw/ehkKgKglMqzxvoFmqb6gbu8xwCCwseH3/KmR+fFHVa8dOENDd/CfaMe3BiLrIn6wt89eeayvpinALN70cBdbjJZgX1R99bBLiMJwFtU7IVJicIwwrY3RkjydayZWBoGpgIs8/a9Ll55GwMko+bmwax9gFGYe5unxTJ/HpmzobVKFlw5fwHG3ulX2Kvnzofnozc4v0bd0eX0Q6OGLOPtWOZq8UUvluOiaCI8DQr8jLEZXvMnV3YDH5F8Jst9P19DAT97GErjjuLT1LsnFQEQyo4fX7Gg1GMEpRm59/okHDWtsB7vHhpXkzYFs7Vh+i9vmfL2UtENBzwHASiuZA4ArYCQa1GT4cQBQ9w+eMOwEsA3GZGT8Rs+ifEk+QMAwzoZ8KcDXFPzGgJGFQDVrdpBXA9LxXShhCknLp6Ikpm4KkUF6BhT6VQS7I2HXmGZdAIAfGUiKdbJUDm/G3CFftZjTwrY+nFjY2Pr7lL9TPNPh389aq8dOmLIbdHfKqti+G1jmw2jcApKq8vU2GQURh2Nf9AjOmyGy+Hrku0t52kPXlXViOH/nfPYAIbmIGNHDkdLoy5s7gT6tG6GwogqQAEK3d1AqhBAOaptskgZAJFLjS9W1iJsAtCd99ihXH/Yz5x+e8Gf7KMr5mw8/pWoTzz+qaF8U/i95uWrrQJwDMae8aOuC60l3OgNvZf33TELZsaK9JXJf/7++lWTfkkbzYFGyCcwmawFcA4tWYflfCtv6dHkmEExHN9mKvt4Hgm8wuU4ja4MW7kW8wcOBar7AZPSXlgEF+HqBndfcFN6TerCCc7VBGmlF9eGCsDaDuD9BzI3y7pmiY7dH97EN9/lDeOCnqKeNe9v1VHg1rZ9dapDyDW5vAQX0JLkPVhAjsS27I4j8FL2YQIAoIKcmXUF5ALcSTLnuKaQlVjD0AgqZ/siO1MiYGafDc0RL/O37jQ6oxN/NyacMeLwW1ZRMLniSKtGWTJe559o1FKyuTQwLuw60heK4fCa6nfCQhMD8lfvVHhYzBN+fx6FDbwHAI7x69mVvfwuPJzSR/KmrJNTuJVbssTX8T1A43GGBrCBABaeNplMaY8QYsNc5PaVn0qbBNLKk9404joEkFIuZiwgNgjDKK6cWOtocxFJWWycUldb+yFu2Ldk0kWv7t+9Z/eBx7KuR3Pqnre+Pbl+362csGf3v02uO3iv9oDLJw3fu2P//r0H5mDN5If379lz4GxoAam1AIZoOwpAY/SYQ8fS430AqMm/eOFYNB6rOmUsCsah9Vh8VIXtBo4fLxkHAEigs63qFABFWeUyCACjcc5/td5oiUfePOLHeorv3XXxV1JGibgowoFLow618qn9+OgyafPFzXui1INRq1+Z+WMH5WDoOUdt4SJnzP1D5kODJFu8XEQuIKfjVr4KAC/xlwNxGgDwK5J0nAtgASPLevg4kzbihbiZu4GmHLAj1w4IPz87sN5vzBdO93/XfZWAO05sU5pwEKEtv0gYzISlKCgVC0sAB0CUOEdx2P5Y11XGBlpnYXPcg4dHSFrgPS7DWSS5aFCSjrp+B+k4AwpfoiUXQWVv3BIAYwY8dufHJwggGXU0dZSmPihoMvHIUSfM0GE9R2R8/NhJkdROgaspBwBODjubgLABSVRWVO8lvZOoGjY54tG+0aVEyMdhAIMH+Qw0AKVRT2t5AX7INxA/xIugARGDRxiRZMibcT6bysTDLdwiGmJwPQMGk/szWGY/BhcdTgCVdYMKyoGAAG6gFHCOuUytfym7EPIJEwO0GTnt8l0vF2H1vmtwDrsXTv/DrmPhX03hofDIrl271ots2H/tlLq6urq66TMrTdnMKTHjmcrZ46Tw5T2LTPXUJWFvrVnH0ADpKAIsTpwYP71WY07tWADhqyydDhRHUZk5BUAVMWVial+/Ml1dAIDmZkAvMH7U2CjGdEcZwGic8XDnsujmCX98be/VPb24bcxfYaP4Y8kp7uWnyx7hst7vnrZ1XRLS6zw178pQZfNMQuBI/8AD6aUFpy/Z8nT79+VWfUYO2JkYjvOGAQOem0XAnRhHDsOj/AUA2clr8L1/iOsHIcAWPgoAH+dgc/jNdotHx3uXnXhDLOpHbd/d/HTkovqauRfXRunyrjgSnskInVP7nowEOpo1ufG1wi94W5uUt1eJds+3bVFDz9WMRAMhV2fV+gU3QQPvcFl2voEk2TcKj/MhANjHb+ffYDnXw+vhvMH3csZATPG1DhCzLkpCj8LRIZnRHmxz6CFUNDIWJSgd5Vs0FsTHpFsFGOF5x/rGDjlS6pny0ojuY6tRUjLS5iqfkI9Di3jyIJ/FiOa+c+J3p3vSzVWyyYXOOZfujVyY6u3tPTX26/Qa8ZRsTd8UW9J3ZHgiLj/JnEy3Vokv16aTpMtHPZAI4QCokng67WJGJyIqMQAQA2AMgCDjxeIMgYKYywTx4p4+wPN9RBED6FgsV2QYQKHmSWOjMVBoO0N+cO/IkM57IVq9TDmh9/iIO1/2IwDHvPsfnfm2dfLzI0ve2fVPJS8kIr1l3pyH/c0B1WvzpqwKlx656wsWIZ9Abdae66GAPXlAnJU1dhO/OGD580hyClZwQ9ZN3YPp2dD7AMaQpfhPhhKadVdM3On9suHrC5+7UAMX1zgNMOLQhHOi2W6LfcnWpdrWfrHj/rASC+c2bJRm51iSqLmEgkh2/EU6UcHF01y2Xs5wElbyaehBONiSVTSB5wcDuSGbypJpALhr4IdjQLL/UACUm0Q2nT99mBVK+EZfMjy0d+jpwWVNDc+NntnzOs4ootCT4vSGsbUTLZIXp99t2fdC6Jmz4u83iW2/QG0sOLWGeQ3n4FdcD62wPbthNV7gfZhNkt/At7gd2E+SPK4B3JNFyLlZd97IRQAmkFVYM5AfAt2dHQBwdESkKCctOjr7tNfK0At1HLEqdrU65VRbdcaPTIse4lqkF4bCwhYztNLPnGLDsbYEQMh1anKGp6qioUVKKVVcUV5eXlYiKKxIKK+ivLQ8gauY7mifW15RWl46tbGjuePHpZfaxpoyXymllC4vfaqrrb3b2q62TC7q9QK9LpkEAPTkNU6lANcBQAPwytHaCQAlVQBcd6eKdyZzhJ2IlwIASgHAaJy7qRjRmpMq68MFiL3/Iwlg7NeuCbzgO82eMGq4GiuqH3zRY+cCLa5+84eLwlAe+FwGYnqvbI341H/4Dl54yzn2Mwufbdk7tIwkxwNYygaghdfnlX+I2wDBX7PUo/AsV2Z/+A0D49QHT3+qNFsw7Cfhr3tFbzaBjrr1V6fblS0+lo98A9MvaltlYTee3K3F8aTdtmXCFT2Es772nPpe8XxohPzdp/pNPyHJyoH5U3w4/3gFWwdF/5f4Q0xh90i8yIehB4CdMIWzB5W37YVo2Z0KZNoQKggYFoXVZ3ohtPnwWBD11kcf9Khsu0NY9/m5JPFe2X4pnqH+p3RaFfNVQP9YhOV8EQD+/A+mvRaXMyLn5vPXrSTJVBUAYCY5Co/lA33GS+VaBMply/RCa1064ycASYfidAEiEwGwSYmVBGlTYNNIpkJF3UMoxrxCFw7rSuQLH1EX7tJOXOXrxQQgruT1ikL+/o55G2jNDc/FM5NeFRJw9sQ56VWzlv+2fm3T2T3f8qkAtkFFly8H9YvBEPS3whqbASDK9ztlZBmQaj4MAG0tQDEQgw9PxxswsnooSqrLk7Zt4OCGjgBQObjN4otyQn+gT1C48u3PrS+DWBjxA1/wLyf2mG0Xx5/Tv+reY95a4q1NLNt5yTcypu/6LuKpA9aDhDcusHlvMwsKgqpuLsRy/hkVfTwPP8qexTfhYwo5KtdiZU0+2T0f/06ShQOK/pqB6W/8Kkh/n1WFPy9v8RHYWLSud282LRvSUj8twpC0d/1RpT563l9ZdFC9hNC478jGjwyHX0YVnpYrHidmOBkAUNLFhVjOTVmxN5JkHIDCFHIifj+AoFcHpd8BL0IMcwYVjwA5K66duGGaAFA2U2sw8rZbHS7oOtwuADEzlojaPyqYrvZ1jarqgj/VhLqppWhCbOuQJjixIQRachV9NLB3Pe5mbvoAFMxHvBgeppCk5ZMY3cc5+BmfR1WSjiuxkKmhAASzBmvIjJfreVETgIuUkbSORDvtqD0TMhBSfGMSQNyIDYE+P/Sc0WFf3LdWKxPCSL5V9fGsQW1nE+HtpeWbhl27rUfDeFp+tuKPtx+vgw5WXHru3lgM68JV09K6c75W9tIDH0wreGb49zcvvW3fNP/FGqeQzWAPDvY2veg6jBB7PgSApMNIKY+SHwJoRnEpgNE4eQCwhwGkxh09iDHDEcXHtB9EGgDE/UPrfvbMxpfjixOvHFdOqL9SaOXQmx4g0ekTHKBgZcduY6GgwhkzWjbHvpx4raHucx0v6fOL+P/x5wI+4+8PWhhY9ncscx1bpQY6wJ8iVYoWWgD8L5Mvhqo523R9AAAAAElFTkSuQmCC"

def hsize(num_bytes):
    if num_bytes >= 1024**3:
        return f"{num_bytes / (1024**3):.2f} ГБ"
    if num_bytes >= 1024**2:
        return f"{num_bytes / (1024**2):.1f} МБ"
    return f"{num_bytes / 1024:.1f} КБ"

def probe_dur(path):
    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        path
    ]
    try:
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True, creationflags=SUBPROCESS_FLAGS)
        return float(res.stdout.strip())
    except (subprocess.SubprocessError, ValueError, OSError):
        return None

def ffmpeg_media_args(w, h, fps):
    vf = f"scale={w}:{h}:force_original_aspect_ratio=decrease,pad={w}:{h}:(ow-iw)/2:(oh-ih)/2:black,setsar=1"
    return [
        "-vf", vf, "-r", str(fps),
        "-c:v", "libx264", "-crf", "26", "-preset", "medium", "-pix_fmt", "yuv420p",
        "-af", "aresample=async=1000", "-c:a", "aac", "-ac", "1", "-b:a", "64k"
    ]

def sample_slice(src, start, dur, out_path, w, h, fps):
    cmd = [
        "ffmpeg", "-v", "error", "-y",
        "-ss", str(int(start)), "-t", str(int(dur)),
        "-i", src,
        "-map", "0:v:0", "-map", "0:a:0?",
        *ffmpeg_media_args(w, h, fps),
        out_path
    ]
    try:
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, creationflags=SUBPROCESS_FLAGS)
        if os.path.exists(out_path):
            sz = os.path.getsize(out_path)
            try:
                os.remove(out_path)
            except OSError:
                pass
            return sz
    except OSError:
        try:
            if os.path.exists(out_path):
                os.remove(out_path)
        except OSError:
            pass
    return 0

def worth_it(src, dur, orig_size, log_fn, w, h, fps):
    with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as tmp:
        sample_file = tmp.name

    sampled_bytes = 0
    sampled_dur = 0
    base = os.path.basename(src)

    log_fn(f"Предварительная проверка (3 среза по 60 сек): {base}...")

    try:
        if dur <= PREVIEW_TRIGGER_SEC:
            slice_dur = dur / 2
            slice_start = dur / 4
            sz = sample_slice(src, slice_start, slice_dur, sample_file, w, h, fps)
            sampled_bytes = sz
            sampled_dur = slice_dur
        else:
            slice_dur = SAMPLE_LEN_SEC
            for pos in SAMPLE_POSITIONS:
                slice_start = dur * pos
                sz = sample_slice(src, slice_start, slice_dur, sample_file, w, h, fps)
                if sz > 0:
                    sampled_bytes += sz
                    sampled_dur += slice_dur

        if sampled_dur > 0 and sampled_bytes > 0:
            est_bytes = int(sampled_bytes * dur / sampled_dur)
            orig_txt = hsize(orig_size)
            est_txt = hsize(est_bytes)

            if est_bytes >= orig_size:
                log_fn(f"Нет смысла, вес файла увеличится (исходный: {orig_txt}, ожидаемый: ~{est_txt}). Пропуск: {base}")
                return False

            log_fn(f"Оценка: исходный {orig_txt} -> ожидаемый ~{est_txt} (сжатие выгодно)")

        return True
    finally:
        try:
            if os.path.exists(sample_file):
                os.remove(sample_file)
        except OSError:
            pass

def encode(src, dst, dur, prog_fn, w, h, fps):
    cmd = [
        "ffmpeg", "-y",
        "-i", src,
        "-map", "0:v:0", "-map", "0:a:0?",
        *ffmpeg_media_args(w, h, fps),
        "-movflags", "+faststart",
        "-progress", "pipe:1",
        dst
    ]
    try:
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            creationflags=SUBPROCESS_FLAGS
        )
        err_lines = []

        def _read_err():
            if proc.stderr:
                for line in proc.stderr:
                    trimmed = line.strip()
                    if trimmed:
                        err_lines.append(trimmed)
                        if len(err_lines) > 10:
                            err_lines.pop(0)

        err_thread = threading.Thread(target=_read_err, daemon=True)
        err_thread.start()

        if proc.stdout:
            for line in proc.stdout:
                line = line.strip()
                if line.startswith("out_time_us=") and dur and dur > 0:
                    try:
                        us = int(line.split("=")[1].strip())
                        pct = min(100.0, max(0.0, (us / 1000000.0 / dur) * 100.0))
                        if prog_fn:
                            prog_fn(pct)
                    except ValueError:
                        pass
                elif line.startswith("progress=end"):
                    if prog_fn:
                        prog_fn(100.0)

        proc.wait()
        err_thread.join(timeout=1.0)
        if proc.returncode == 0:
            return True, ""
        err_msg = err_lines[-1] if err_lines else f"код ошибки {proc.returncode}"
        return False, err_msg
    except OSError as e:
        return False, str(e)

def add_copy_row(parent, text):
    frame = tk.Frame(parent, relief="solid", bd=1, padx=8, pady=4)
    btn = tk.Button(frame, text="Копировать", width=12)
    def copy():
        frame.clipboard_clear()
        frame.clipboard_append(text)
        btn.config(text="Скопировано!")
        frame.after(1500, lambda: btn.config(text="Копировать"))
    btn.config(command=copy)
    btn.pack(side="right", padx=(8, 0))

    lbl = tk.Label(frame, text=text, font="TkFixedFont", anchor="w", justify="left", wraplength=380)
    lbl.pack(side="left", fill="x", expand=True)
    return frame

CACHED_IMAGES = {}

def get_qr_image(master):
    local_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "my_QR.png")
    if os.path.exists(local_path):
        try:
            full = tk.PhotoImage(master=master, file=local_path)
            sub = full.subsample(5, 5)
            CACHED_IMAGES["qr_full"] = full
            CACHED_IMAGES["qr_sub"] = sub
            return sub
        except Exception:
            pass
    img = tk.PhotoImage(master=master, data=QR_CODE_DATA)
    CACHED_IMAGES["qr_img"] = img
    return img

def get_tg_image(master):
    img = tk.PhotoImage(master=master, data=TG_ICON_DATA)
    CACHED_IMAGES["tg_img"] = img
    return img

def get_gh_image(master):
    img = tk.PhotoImage(master=master, data=GH_ICON_DATA)
    CACHED_IMAGES["gh_img"] = img
    return img

class GuideWindow:
    def __init__(self, parent):
        self.win = tk.Toplevel(parent)
        self.win.title("Руководство по установке FFmpeg")
        self.win.geometry("564x846")
        self.win.resizable(False, False)
        self.win.transient(parent)
        self.setup()

    def setup(self):
        bottom = tk.Frame(self.win)
        bottom.pack(side="bottom", fill="x", padx=16, pady=(0, 10))
        tk.Label(bottom, text="Версия приложения 1.2", fg="gray").pack(side="left")
        tk.Button(bottom, text="Закрыть", width=12, command=self.win.destroy).pack(side="right")

        body = tk.Frame(self.win, padx=16, pady=8)
        body.pack(side="top", fill="both", expand=True)
        self.fill(body)

    def fill(self, body):
        tk.Label(body, text="1. Быстрый способ (через консоль Windows):", font=("TkDefaultFont", 10, "bold"), anchor="w").pack(fill="x", pady=(0, 2))
        tk.Label(body, text="Откройте PowerShell или командную строку и выполните команду:", anchor="w").pack(fill="x", pady=(0, 2))
        add_copy_row(body, "winget install Gyan.FFmpeg").pack(fill="x", pady=(0, 2))
        tk.Label(body, text="После завершения установки перезапустите эту программу.", anchor="w").pack(fill="x", pady=(0, 8))

        tk.Label(body, text="2. Ручной способ:", font=("TkDefaultFont", 10, "bold"), anchor="w").pack(fill="x", pady=(0, 2))
        site_row = tk.Frame(body)
        site_row.pack(fill="x", pady=(0, 2))
        tk.Label(site_row, text="Скачайте архив с сайта: ", anchor="w").pack(side="left")
        site_link = tk.Label(site_row, text="ffmpeg.download", fg="blue", cursor="hand2", font=("TkDefaultFont", 10, "underline"))
        site_link.pack(side="left")
        site_link.bind("<Button-1>", lambda _e: webbrowser.open_new_tab("https://ffmpeg.download"))

        tk.Label(body, text="Распакуйте его в удобное место (например, в C:\\ffmpeg).", anchor="w").pack(fill="x", pady=(0, 2))
        tk.Label(body, text="Добавьте папку bin (C:\\ffmpeg\\bin) в переменную PATH.", anchor="w").pack(fill="x", pady=(0, 4))

        tk.Label(body, text="Быстрая команда в PowerShell:", anchor="w").pack(fill="x", pady=(0, 2))
        add_copy_row(body, '[Environment]::SetEnvironmentVariable("Path", [Environment]::GetEnvironmentVariable("Path", "User") + ";C:\\ffmpeg\\bin", "User")').pack(fill="x", pady=(0, 6))

        tk.Label(body, text="Или команда в командной строке (CMD):", anchor="w").pack(fill="x", pady=(0, 2))
        add_copy_row(body, 'setx PATH "%PATH%;C:\\ffmpeg\\bin"').pack(fill="x", pady=(0, 6))

        tk.Label(body, text="Или вручную через графическое окно (Win + R):", anchor="w").pack(fill="x", pady=(0, 2))
        add_copy_row(body, "sysdm.cpl").pack(fill="x", pady=(0, 6))

        tk.Label(body, text="- Нажмите Enter, перейдите на вкладку Дополнительно -> Переменные среды.", anchor="w").pack(fill="x")
        tk.Label(body, text="- В блоке Системные переменные найдите строку Path, нажмите Изменить и добавьте путь к bin.", anchor="w", justify="left", wraplength=520).pack(fill="x", pady=(0, 6))

        tk.Label(body, text="3. Проверка:", font=("TkDefaultFont", 10, "bold"), anchor="w").pack(fill="x", pady=(0, 2))
        tk.Label(body, text="Откройте командную строку и выполните команду:", anchor="w").pack(fill="x", pady=(0, 2))
        add_copy_row(body, "ffmpeg -version").pack(fill="x", pady=(0, 2))
        tk.Label(body, text="Если в терминале отобразилась версия, установка завершена.", anchor="w").pack(fill="x", pady=(0, 8))

        support_frame = tk.Frame(body, bg="#f8fafc", padx=10, pady=8, highlightbackground="#cbd5e1", highlightcolor="#cbd5e1", highlightthickness=1)
        support_frame.pack(fill="x", pady=(4, 0))

        tk.Label(support_frame, text="Буду благодарен любой поддержке! <3", font=("TkDefaultFont", 10, "bold"), fg="#0f172a", bg="#f8fafc").pack(anchor="w", pady=(0, 2))

        support_row = tk.Frame(support_frame, bg="#f8fafc")
        support_row.pack(fill="x")

        support_left = tk.Frame(support_row, bg="#f8fafc")
        support_left.pack(side="left", fill="both", expand=True)

        tk.Label(
            support_left,
            text="Если программа вам полезна, вы можете поддержать проект или задать вопрос автору:",
            font=("TkDefaultFont", 9),
            fg="#475569",
            bg="#f8fafc",
            justify="left",
            wraplength=370
        ).pack(anchor="w")

        contacts_box = tk.Frame(support_left, bg="#f8fafc")
        contacts_box.pack(anchor="w", pady=(3, 3))

        tg_row = tk.Frame(contacts_box, bg="#f8fafc")
        tg_row.pack(anchor="w", pady=(0, 2))
        self.tg_img = get_tg_image(self.win)
        CACHED_IMAGES["tg"] = self.tg_img
        tg_lbl = tk.Label(tg_row, image=self.tg_img, bg="#f8fafc")
        tg_lbl.image = self.tg_img
        tg_lbl.pack(side="left", padx=(0, 5))
        tk.Label(
            tg_row,
            text="Связь с автором в Telegram:",
            font=("TkDefaultFont", 9),
            fg="#334155",
            bg="#f8fafc"
        ).pack(side="left", padx=(0, 4))
        tg_link = tk.Label(
            tg_row,
            text="@sudo_ai",
            font=("TkDefaultFont", 9, "bold"),
            fg="#2563eb",
            bg="#f8fafc",
            cursor="hand2"
        )
        tg_link.pack(side="left")
        tg_link.bind("<Button-1>", lambda _e: webbrowser.open_new_tab("https://t.me/sudo_ai"))

        gh_row = tk.Frame(contacts_box, bg="#f8fafc")
        gh_row.pack(anchor="w", pady=(2, 0))
        self.gh_img = get_gh_image(self.win)
        CACHED_IMAGES["gh"] = self.gh_img
        gh_lbl = tk.Label(gh_row, image=self.gh_img, bg="#f8fafc")
        gh_lbl.image = self.gh_img
        gh_lbl.pack(side="left", padx=(0, 5))
        tk.Label(
            gh_row,
            text="Профиль на GitHub:",
            font=("TkDefaultFont", 9),
            fg="#334155",
            bg="#f8fafc"
        ).pack(side="left", padx=(0, 4))
        gh_link = tk.Label(
            gh_row,
            text="git-sudo-ai",
            font=("TkDefaultFont", 9, "bold"),
            fg="#2563eb",
            bg="#f8fafc",
            cursor="hand2"
        )
        gh_link.pack(side="left")
        gh_link.bind("<Button-1>", lambda _e: webbrowser.open_new_tab("https://github.com/git-sudo-ai"))

        tk.Label(
            support_left,
            text="Перевод через СБП по QR-коду справа ➔",
            font=("TkDefaultFont", 8),
            fg="#64748b",
            bg="#f8fafc"
        ).pack(anchor="w")

        self.qr_img = get_qr_image(self.win)
        CACHED_IMAGES["qr"] = self.qr_img
        qr_frame = tk.Frame(support_row, bg="#ffffff", padx=2, pady=2, highlightbackground="#cbd5e1", highlightcolor="#cbd5e1", highlightthickness=1)
        qr_frame.pack(side="right", padx=(8, 0))
        qr_lbl = tk.Label(qr_frame, image=self.qr_img, bg="#ffffff")
        qr_lbl.image = self.qr_img
        qr_lbl.pack()
        tk.Label(qr_frame, text="СБП", font=("TkDefaultFont", 7, "bold"), fg="#64748b", bg="#ffffff").pack()

class App:
    def __init__(self, root):
        self.root = root
        self.src_var = tk.StringVar()
        self.res_var = tk.StringVar(value=DEFAULT_RES_KEY)
        self.fps_var = tk.StringVar(value=DEFAULT_FPS_KEY)
        self.is_busy = False
        self.last_dir = None
        self.guide_win = None

        self.root.title("ConvAfterOBS v1.2")
        self.root.geometry("540x412")
        self.root.minsize(460, 360)

        self.setup()
        if len(sys.argv) > 1 and os.path.isfile(sys.argv[1]):
            self.src_var.set(sys.argv[1])

    def setup(self):
        top = tk.Frame(self.root)
        top.pack(fill="x", padx=10, pady=(8, 4))

        head_row = tk.Frame(top)
        head_row.pack(fill="x", pady=(0, 2))
        self.guide_btn = tk.Button(head_row, text="Руководство", width=10, command=self.open_guide)
        self.guide_btn.pack(side="right")

        entry_row = tk.Frame(top)
        entry_row.pack(fill="x", pady=2)
        tk.Label(entry_row, text="Путь:").pack(side="left", padx=(0, 6))
        self.entry = tk.Entry(entry_row, textvariable=self.src_var)
        self.entry.pack(side="left", fill="x", expand=True, padx=(0, 6))
        self.entry.bind("<Return>", lambda _e: self.start_conversion())

        self.browse_btn = tk.Button(entry_row, text="Обзор...", width=10, command=self.browse)
        self.browse_btn.pack(side="right")

        opts_row = tk.Frame(top)
        opts_row.pack(fill="x", pady=(4, 6))
        tk.Label(opts_row, text="Разрешение:").pack(side="left", padx=(0, 4))
        self.res_cb = ttk.Combobox(opts_row, textvariable=self.res_var, values=list(RES.keys()), state="readonly", width=17)
        self.res_cb.pack(side="left", padx=(0, 10))

        tk.Label(opts_row, text="Частота кадров:").pack(side="left", padx=(0, 4))
        self.fps_cb = ttk.Combobox(opts_row, textvariable=self.fps_var, values=list(FPS.keys()), state="readonly", width=10)
        self.fps_cb.pack(side="left")

        act_row = tk.Frame(top)
        act_row.pack(fill="x", pady=(2, 0))
        self.convert_btn = tk.Label(
            act_row, text="Конвертировать",
            bg=COLOR_GREEN, fg="white",
            relief="flat", cursor="hand2",
            font=("TkDefaultFont", 10, "bold"),
            pady=7
        )
        self.convert_btn.pack(fill="x", expand=True)
        self.convert_btn.bind("<Button-1>", lambda _e: self.start_conversion())
        self.convert_btn.bind("<Enter>", lambda _e: self.convert_btn.config(bg=COLOR_GREEN_HOVER) if not self.is_busy else None)
        self.convert_btn.bind("<Leave>", lambda _e: self.convert_btn.config(bg=COLOR_GREEN) if not self.is_busy else None)

        prog_row = tk.Frame(top)
        prog_row.pack(fill="x", pady=(6, 2))
        self.prog_bar = ttk.Progressbar(prog_row, orient="horizontal", mode="determinate", maximum=100.0)
        self.prog_bar.pack(side="left", fill="x", expand=True, padx=(0, 8))
        self.prog_lbl = tk.Label(prog_row, text="0%", width=4, anchor="e")
        self.prog_lbl.pack(side="right")

        warn_lbl = tk.Label(
            top,
            text="Внимание: при конвертации записей из Zoom, Телемоста и т.п. проверяйте начало, середину и окончание готового видео.",
            fg=COLOR_WARNING, justify="left", wraplength=500
        )
        warn_lbl.pack(fill="x", pady=(4, 2))
        top.bind("<Configure>", lambda e: warn_lbl.config(wraplength=max(200, e.width - 10)))

        log_frame = tk.Frame(self.root)
        log_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        tk.Label(log_frame, text="Журнал событий:", anchor="w").pack(fill="x", pady=(0, 2))
        self.log_box = scrolledtext.ScrolledText(log_frame, wrap="word", height=6, state="disabled")
        self.log_box.pack(fill="both", expand=True)

    def open_guide(self):
        try:
            if self.guide_win is None or not self.guide_win.win.winfo_exists():
                self.guide_win = GuideWindow(self.root)
            else:
                self.guide_win.win.lift()
        except Exception:
            self.guide_win = GuideWindow(self.root)

    def browse(self):
        f = filedialog.askopenfilename(
            initialdir=self.last_dir,
            filetypes=[("Видео файлы", "*.mp4 *.mkv *.mov *.avi *.webm *.flv *.m4v *.MP4 *.MKV *.MOV *.AVI *.WEBM *.FLV *.M4V"), ("Все файлы", "*.*")]
        )
        if f:
            self.last_dir = os.path.dirname(f)
            self.src_var.set(f)

    def start_conversion(self):
        if self.is_busy:
            return

        src = self.src_var.get().strip().strip('"').strip("'")
        if not src:
            self.log("Укажите путь к файлу.")
            return

        if not shutil.which("ffmpeg"):
            self.log("Ошибка: ffmpeg не найден в системе (PATH).")
            return

        if not os.path.isfile(src):
            self.log(f"Файл не найден: {src}")
            return

        res_choice = self.res_var.get()
        w, h = RES[res_choice] if res_choice in RES else RES[DEFAULT_RES_KEY]
        fps_choice = self.fps_var.get()
        fps = FPS[fps_choice] if fps_choice in FPS else FPS[DEFAULT_FPS_KEY]

        self.set_progress(0.0)
        self.set_busy(True)

        def worker():
            try:
                self.process(src, w, h, fps)
            finally:
                def _done():
                    self.set_busy(False)
                    self.root.title("ConvAfterOBS v1.2")
                self.root.after(0, _done)

        threading.Thread(target=worker, daemon=True).start()

    def process(self, src, w, h, fps):
        src_norm = os.path.abspath(src)
        src_lower = src_norm.lower()
        if src_lower.endswith("_converted.mp4") or src_lower.endswith("_temp.mp4"):
            return

        parent_dir = os.path.dirname(src_norm)
        stem = os.path.splitext(os.path.basename(src_norm))[0]
        final_dst = os.path.join(parent_dir, f"{stem}_converted.mp4")
        temp_dst = os.path.join(parent_dir, f"{stem}_temp.mp4")

        if os.path.exists(final_dst):
            self.log(f"Пропуск (уже существует): {final_dst}")
            return

        try:
            orig_size = os.path.getsize(src_norm)
        except OSError:
            self.log(f"Не удалось прочитать размер: {src_norm}")
            return

        dur = probe_dur(src_norm)

        if dur and dur > 60 and orig_size > 0:
            if not worth_it(src_norm, dur, orig_size, self.log, w, h, fps):
                return

        fps_suf = "кадра" if fps == 24 else "кадров"
        self.log(f"Конвертация ({w}x{h}, {fps} {fps_suf}): {os.path.basename(src_norm)}")
        try:
            if os.path.exists(temp_dst):
                os.remove(temp_dst)
        except OSError:
            pass

        ok, err = encode(src_norm, temp_dst, dur, self.set_progress, w, h, fps)
        if not ok or not os.path.exists(temp_dst):
            try:
                if os.path.exists(temp_dst):
                    os.remove(temp_dst)
            except OSError:
                pass
            err_text = f": {err}" if err else ""
            self.log(f"Ошибка при конвертации ({os.path.basename(src_norm)}){err_text}")
            return

        try:
            new_size = os.path.getsize(temp_dst)
        except OSError:
            new_size = 0

        orig_txt = hsize(orig_size)
        new_txt = hsize(new_size)

        if new_size >= orig_size:
            try:
                if os.path.exists(temp_dst):
                    os.remove(temp_dst)
            except OSError:
                pass
            self.log(f"Нет смысла, вес файла увеличится (исходный: {orig_txt}, сжатый: {new_txt}). Файл отменен.")
            return

        try:
            if os.path.exists(final_dst):
                os.remove(final_dst)
            os.replace(temp_dst, final_dst)
            self.log(f"Файл успешно сохранен: {final_dst} ({orig_txt} -> {new_txt})")
        except OSError as e:
            try:
                if os.path.exists(temp_dst):
                    os.remove(temp_dst)
            except OSError:
                pass
            self.log(f"Ошибка сохранения файла: {e}")

    def set_busy(self, busy):
        self.is_busy = busy
        st = "disabled" if busy else "normal"
        cb_st = "disabled" if busy else "readonly"
        self.convert_btn.config(
            bg="#9e9e9e" if busy else COLOR_GREEN,
            cursor="arrow" if busy else "hand2"
        )
        self.browse_btn.config(state=st)
        self.guide_btn.config(state=st)
        self.entry.config(state=st)
        self.res_cb.config(state=cb_st)
        self.fps_cb.config(state=cb_st)

    def set_progress(self, pct):
        def _update():
            self.prog_bar.config(value=pct)
            self.prog_lbl.config(text=f"{int(pct)}%")
            self.root.title(f"ConvAfterOBS v1.2 - {int(pct)}%")
        self.root.after(0, _update)

    def log(self, text):
        def _append():
            self.log_box.config(state="normal")
            self.log_box.insert("end", text + "\n")
            self.log_box.see("end")
            self.log_box.config(state="disabled")
        self.root.after(0, _append)

def main():
    root = tk.Tk()
    App(root)
    root.mainloop()

if __name__ == "__main__":
    main()
