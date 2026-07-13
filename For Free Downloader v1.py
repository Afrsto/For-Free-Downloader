import sys
import os
import json
import urllib.request
import urllib.parse
import urllib.error
import threading
import re
import time
import webbrowser
import winreg
import subprocess
import zipfile
import tempfile
import shutil
import ctypes
import tkinter as tk
from tkinter import messagebox, filedialog, Toplevel, Listbox, Scrollbar, END, SINGLE, StringVar

import customtkinter as ctk

def is_admin() -> bool:
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    script = os.path.abspath(sys.argv[0])
    params = ' '.join(sys.argv[1:])
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, f'"{script}" {params}', None, 1)

if not is_admin():
    run_as_admin()
    sys.exit(0)

APP_TITLE   = "For Free Downloader"
APP_VERSION = "1"
APP_AUTHOR  = "X2"

LANG = "en"

STRINGS = {
    "en": {
        "tab_patcher":        "Steam",
        "tab_about":          "ℹ About",
        "section_appid":      "Steam App ID",
        "section_actions":    "Actions",
        "section_password":   "Online Fix Password",
        "section_progress":   "Progress",
        "section_log":        "Activity Log",
        "btn_remove_all":     "🗑 Remove All Games",
        "btn_search":         "🔍 Search Game",
        "btn_download":       "⬇ Download & Extract",
        "btn_online_fix":     "🔧 Online Fix",
        "btn_update":         "⚙ Update",
        "btn_steam_folder":   "📁 Steam Folder",
        "btn_remove_game":    "🗑 Remove Game",
        "btn_restart_steam":  "♻ Restart Steam",
        "btn_fix_steamtools": "🛠 Fix SteamTools",
        "btn_copy":           "📋 Copy",
        "btn_copy_log":       "📋 Copy Log",
        "btn_lang":           "🌐 عربي",
        "btn_dl_steamtools":  "⬇ Download SteamTools",
        "btn_run_steamtools": "▶ Run SteamTools",
        "tip_remove_all":     "Delete ALL game files (lua & manifest) from Steam",
        "tip_search":         "Search the Steam store and auto-fill the App ID",
        "tip_download":       "Download and extract manifest files to Steam folders",
        "tip_online_fix":     "Open the Online Fix repair page for this game",
        "tip_update":         "Open the Game Updates manager",
        "tip_steam_folder":   "Select your Steam installation folder",
        "tip_remove_game":    "Delete all game files for the entered App ID",
        "tip_restart_steam":  "Kill and restart Steam",
        "tip_fix_steamtools": "Download OpenSteamTool and place DLLs in Steam folder",
        "tip_dl_steamtools":  "Download and run the SteamTools installer",
        "tip_copy_pw":        "Copy the password to clipboard",
        "id_placeholder":     "e.g. 730 (CS2)",
        "log_ready":          "Ready — enter or search for an App ID to begin.\n",
        "idle":               "Idle",
        "copied":             "✓ Copied!",
        "log_copied":         "  Log copied to clipboard.",
        "about_title":        APP_TITLE,
        "about_version":      f"Version {APP_VERSION}  •  by {APP_AUTHOR}",
        "about_info": (
            "X2 Salah Downloader lets you:\n\n"
            "  🔍  Search for any Steam game and auto-fill its App ID\n"
            "  📥  Download the manifest ZIP for a given App ID\n"
            "  🔧  Open the Online Fix repair page for a game\n"
            "  📋  Quickly copy the Online Fix password\n"
            "  🧹  Remove all game files for a specific game or all games\n"
            "  ⚙️  Update (patch .lua files) — disables forced updates\n\n"
            "All functionality is consolidated into one modern tool."
        ),
        "about_telegram":     "Telegram — X2 Salah",
        "searching":          "Searching...",
        "downloading":        "  Downloading...",
        "no_appid_warn":      "No App ID",
        "no_appid_msg":       "Please enter or search for an App ID first.",
        "invalid_appid":      "Invalid App ID",
        "invalid_appid_msg":  "App ID must be a numeric value.",
        "dl_fail_title":      "Download Failed",
        "dl_ok_title":        "Download Complete",
        "dl_ok_msg":          "Game files extracted and installed to Steam successfully.",
        "extract_fail":       "Extraction Failed",
        "extract_fail_msg":   "Could not extract the downloaded file:\n\n{err}",
        "done_opened":        "  Done! Files moved to Steam.",
        "dl_failed_lbl":      "  Download failed.",
        "extracting":         "  Extracting files...",
        "steam_not_found":    "Steam installation not found.",
        "error":              "Error",
        "done":               "Done",
        "no_steam_folder":    "No Steam Folder",
        "no_steam_msg":       "Steam folder not found.\nClick 'Steam Folder' to set it.",
        "no_steam_msg2":      "Steam folder not set.\nClick 'Steam Folder' to set it.",
        "invalid_path":       "Invalid Path",
        "invalid_path_msg":   "Steam.exe not found in:\n{path}",
        "remove_all_confirm": "Remove ALL Games?",
        "remove_all_msg":     "This will delete ALL .lua files from config\\lua\nand .manifest files from config\\depotcache\nin your Steam folder.\n\nAre you sure?",
        "remove_all_done":    "Done",
        "remove_all_done_msg": "Removed {n} game file(s) from your Steam folder.",
        "removal_complete":   "Removal Complete",
        "no_files_found":     "No Files Found",
        "no_files_msg":       "No game files found for {label}.",
        "confirm_removal":    "Confirm Removal",
        "confirm_removal_msg": "Delete all game files for:\n\n  {label}\n\nThis cannot be undone. Continue?",
        "remove_done_title":  "✅ Removal Complete",
        "remove_done_msg":    "Successfully removed {n} file(s) for:\n\n  {label}",
        "remove_none_title":  "No Files Found",
        "remove_none_msg":    "No game files were found for:\n\n  {label}",
        "restart_error":      "Could not restart Steam:\n{err}",
        "fix_st_running":     "  Installing OpenSteamTool...",
        "fix_st_done":        "  OpenSteamTool installed (DLLs placed in Steam folder).",
        "steam_path_label":   "Steam:",
        "steam_path_notfound": "Steam folder not found — click 'Steam Folder' to set it",
        "dir_select":         "Select folder to extract game files into",
        "search_dialog_title": "Steam Game Search",
        "search_placeholder": "Enter game name...",
        "search_btn":         "🔍 Search",
        "select_game":        "✅ Select Game",
        "cancel":             "❌ Cancel",
        "filter_placeholder": "Filter by game name...",
        "remove_game_title":  "Remove Game",
        "scanning":           "Scanning installed games...",
        "pw_label":           "online-fix.me",

        "update_manager_title": "Game Updates",
        "update_all": "⚙️ Update All",
        "close": "❌ Close",
        "total_games": "Total Games: {n}",
        "updates_available": "Updates Available: {n}",
        "up_to_date": "Up to date",
        "update_available": "Update available",
        "updating": "Updating...",
        "updated_success": "✅ Updated successfully",
        "failed": "❌ Failed",
        "skipped": "⏭️ Cancelled",
        "cancel_update": "❌ Disable",
        "update_language": "✅ Enable",
        "update_complete": "Update Complete",
        "summary_text": "Updated Successfully: {updated}\nCancelled: {skipped}\nFailed: {failed}\nAlready Updated: {already}",
        "scanning_games": "Scanning installed games...",
        "no_games_found": "No installed games found.",
        "update_all_confirm": "Patch all .lua files?",
        "update_all_msg": "This will patch ALL .lua files to disable forced updates.\nGames already patched will be skipped.\n\nContinue?",
        "downloading_installer": "Downloading OpenSteamTool...",
        "downloaded_installer": "Download complete, extracting DLLs...",
        "installer_download_failed": "Failed to download OpenSteamTool.",
        "installer_launch_failed": "Failed to extract DLLs.",
        "installer_download_progress": "Downloading: {downloaded} / {total}",
        "installer_download_complete": "Downloaded successfully.",
        "installer_launching": "Extracting DLLs...",
        "uncancel": "Enable",
        "search_games": "🔍 Search here for the game name or App ID",
        "search_games_tooltip": "Type a game name or App ID to filter the list.",
        "update_btn_tooltip": "Enable (patch) this game to disable forced updates.",
        "disable_btn_tooltip": "Disable (revert) this game to allow forced updates.",
        "update_all_tooltip": "Patch all .lua files (disable forced updates).",
        "auto_update_on": "Enabled (patched)",
        "auto_update_off": "Disabled (unpatched)",
        "manifest_not_found": "Game not installed",
        "migrating": "Migrating old .lua files from stplug-in to config\\lua...",
        "migrated": "Migration complete: {n} file(s) moved.",
        "no_match_search": "No games match your search.",
    },
    "ar": {
        "tab_patcher":        "ستيم",
        "tab_about":          "ℹ حول",
        "section_appid":      "معرّف تطبيق ستيم",
        "section_actions":    "الإجراءات",
        "section_password":   "كلمة مرور Online Fix",
        "section_progress":   "التقدم",
        "section_log":        "سجل النشاط",
        "btn_remove_all":     "🗑 حذف جميع الألعاب",
        "btn_search":         "🔍 بحث عن لعبة",
        "btn_download":       "⬇ تحميل واستخراج",
        "btn_online_fix":     "🔧 إصلاح أونلاين",
        "btn_update":         "⚙ تحديث",
        "btn_steam_folder":   "📁 مجلد ستيم",
        "btn_remove_game":    "🗑 حذف لعبة",
        "btn_restart_steam":  "♻ إعادة تشغيل ستيم",
        "btn_fix_steamtools": "🛠 SteamTools إصلاح",
        "btn_copy":           "📋 نسخ",
        "btn_copy_log":       "📋 نسخ السجل",
        "btn_lang":           "🌐 English",
        "btn_dl_steamtools":  "⬇ SteamTools تحميل",
        "btn_run_steamtools": "▶ SteamTools تشغيل",
        "tip_remove_all":     "حذف جميع ملفات اللعبة من مجلد ستيم",
        "tip_search":         "البحث في متجر ستيم وملء معرّف التطبيق تلقائياً",
        "tip_download":       "تحميل واستخراج ملفات المانيفست إلى مجلدات ستيم",
        "tip_online_fix":     "فتح صفحة إصلاح Online Fix لهذه اللعبة",
        "tip_update":         "فتح مدير التحديثات",
        "tip_steam_folder":   "اختر مجلد تثبيت ستيم",
        "tip_remove_game":    "حذف جميع ملفات اللعبة للمعرّف المدخل",
        "tip_restart_steam":  "إيقاف وإعادة تشغيل ستيم",
        "tip_fix_steamtools": "تحميل OpenSteamTool ووضع ملفات DLL في مجلد ستيم",
        "tip_dl_steamtools":  "تحميل وتشغيل مثبت SteamTools",
        "tip_copy_pw":        "نسخ كلمة المرور إلى الحافظة",
        "id_placeholder":     "مثال: 730 (CS2)",
        "log_ready":          "جاهز — أدخل أو ابحث عن معرّف التطبيق للبدء.\n",
        "idle":               "في انتظار",
        "copied":             "✓ تم النسخ!",
        "log_copied":         "  تم نسخ السجل إلى الحافظة.",
        "about_title":        APP_TITLE,
        "about_version":      f"الإصدار {APP_VERSION}  •  بواسطة {APP_AUTHOR}",
        "about_info": (
            "X2 Salah Downloader يتيح لك:\n\n"
            "  🔍  البحث عن أي لعبة ستيم وملء معرّفها تلقائياً\n"
            "  📥  تحميل ملف ZIP للمانيفست لمعرّف التطبيق\n"
            "  🔧  فتح صفحة إصلاح Online Fix للعبة\n"
            "  📋  نسخ كلمة مرور Online Fix بسرعة\n"
            "  🧹  حذف ملفات اللعبة للعبة أو لجميع الألعاب\n"
            "  ⚙️  تحديث (تصحيح ملفات .lua) — يعطّل التحديثات الإجبارية\n\n"
            "جميع الوظائف موحّدة في أداة واحدة حديثة."
        ),
        "about_telegram":     "تيليغرام — X2 Salah",
        "searching":          "جاري البحث...",
        "downloading":        "  جاري التحميل...",
        "no_appid_warn":      "لا يوجد معرّف",
        "no_appid_msg":       "الرجاء إدخال أو البحث عن معرّف التطبيق أولاً.",
        "invalid_appid":      "معرّف غير صالح",
        "invalid_appid_msg":  "يجب أن يكون معرّف التطبيق رقمياً.",
        "dl_fail_title":      "فشل التحميل",
        "dl_ok_title":        "اكتمل التحميل",
        "dl_ok_msg":          "تم استخراج ملفات اللعبة بنجاح إلى مجلدات ستيم.",
        "extract_fail":       "فشل الاستخراج",
        "extract_fail_msg":   "تعذّر استخراج الملف المحمّل:\n\n{err}",
        "done_opened":        "  تم! تم نقل الملفات إلى ستيم.",
        "dl_failed_lbl":      "  فشل التحميل.",
        "extracting":         "  جاري الاستخراج...",
        "steam_not_found":    "لم يتم العثور على تثبيت ستيم.",
        "error":              "خطأ",
        "done":               "تم",
        "no_steam_folder":    "لا يوجد مجلد ستيم",
        "no_steam_msg":       "مجلد ستيم غير موجود.\nانقر على 'مجلد ستيم' لتحديده.",
        "no_steam_msg2":      "مجلد ستيم غير محدد.\nانقر على 'مجلد ستيم' لتحديده.",
        "invalid_path":       "مسار غير صالح",
        "invalid_path_msg":   "لم يتم العثور على Steam.exe في:\n{path}",
        "remove_all_confirm": "حذف جميع الألعاب؟",
        "remove_all_msg":     "سيؤدي هذا إلى حذف جميع ملفات .lua من config\\lua\nوملفات .manifest من config\\depotcache\nفي مجلد ستيم.\n\nهل أنت متأكد؟",
        "remove_all_done":    "تم",
        "remove_all_done_msg": "تم حذف {n} ملف(ات) من مجلد ستيم.",
        "removal_complete":   "اكتمل الحذف",
        "no_files_found":     "لم يتم العثور على ملفات",
        "no_files_msg":       "لم يتم العثور على ملفات لـ {label}.",
        "confirm_removal":    "تأكيد الحذف",
        "confirm_removal_msg": "حذف جميع ملفات اللعبة لـ:\n\n  {label}\n\nلا يمكن التراجع. هل تريد المتابعة؟",
        "remove_done_title":  "✅ اكتمل الحذف",
        "remove_done_msg":    "تم حذف {n} ملف(ات) بنجاح لـ:\n\n  {label}",
        "remove_none_title":  "لم يتم العثور على ملفات",
        "remove_none_msg":    "لم يتم العثور على ملفات لـ:\n\n  {label}",
        "restart_error":      "تعذّر إعادة تشغيل ستيم:\n{err}",
        "fix_st_running":     "  جاري تثبيت OpenSteamTool...",
        "fix_st_done":        "  تم تثبيت OpenSteamTool (تم نقل ملفات DLL إلى مجلد ستيم).",
        "steam_path_label":   "ستيم:",
        "steam_path_notfound": "مجلد ستيم غير موجود — انقر على 'مجلد ستيم' لتحديده",
        "dir_select":         "اختر مجلداً لاستخراج ملفات اللعبة فيه",
        "search_dialog_title": "بحث في ستيم",
        "search_placeholder": "أدخل اسم اللعبة...",
        "search_btn":         "🔍 بحث",
        "select_game":        "✅ اختر اللعبة",
        "cancel":             "❌ إلغاء",
        "filter_placeholder": "فلترة باسم اللعبة...",
        "remove_game_title":  "حذف لعبة",
        "scanning":           "جاري المسح...",
        "pw_label":           "online-fix.me",

        "update_manager_title": "تحديثات الألعاب",
        "update_all": "⚙️ تحديث الكل",
        "close": "❌ إغلاق",
        "total_games": "إجمالي الألعاب: {n}",
        "updates_available": "تحديثات متاحة: {n}",
        "up_to_date": "محدث",
        "update_available": "تحديث متاح",
        "updating": "جاري التحديث...",
        "updated_success": "✅ تم التحديث بنجاح",
        "failed": "❌ فشل",
        "skipped": "⏭️ تم الإلغاء",
        "cancel_update": "❌ تعطيل",
        "update_language": "✅ تفعيل",
        "update_complete": "اكتمل التحديث",
        "summary_text": "تم التحديث بنجاح: {updated}\nتم الإلغاء: {skipped}\nفشل: {failed}\nمحدث بالفعل: {already}",
        "scanning_games": "جاري مسح الألعاب المثبتة...",
        "no_games_found": "لم يتم العثور على ألعاب مثبتة.",
        "update_all_confirm": "تصحيح جميع ملفات .lua؟",
        "update_all_msg": "سيتم تصحيح جميع ملفات .lua لتعطيل التحديثات الإجبارية.\nسيتم تخطي الألعاب المصححة بالفعل.\n\nهل تريد المتابعة؟",
        "downloading_installer": "جاري تحميل OpenSteamTool...",
        "downloaded_installer": "اكتمل التحميل، جاري استخراج ملفات DLL...",
        "installer_download_failed": "فشل تحميل OpenSteamTool.",
        "installer_launch_failed": "فشل استخراج ملفات DLL.",
        "installer_download_progress": "جاري التحميل: {downloaded} / {total}",
        "installer_download_complete": "تم التحميل بنجاح.",
        "installer_launching": "جاري استخراج ملفات DLL...",
        "uncancel": "تفعيل",
        "search_games": "🔍 ابحث هنا باسم اللعبة أو المعرف",
        "search_games_tooltip": "اكتب اسم اللعبة أو معرف التطبيق لتصفية القائمة.",
        "update_btn_tooltip": "تفعيل (تصحيح) هذه اللعبة لتعطيل التحديثات الإجبارية.",
        "disable_btn_tooltip": "تعطيل (تراجع) هذه اللعبة للسماح بالتحديثات الإجبارية.",
        "update_all_tooltip": "تصحيح جميع ملفات .lua (تعطيل التحديثات الإجبارية).",
        "auto_update_on": "مفعّل (مصحح)",
        "auto_update_off": "معطّل (غير مصحح)",
        "manifest_not_found": "اللعبة غير مثبّتة",
        "migrating": "جاري ترحيل ملفات .lua القديمة من stplug-in إلى config\\lua...",
        "migrated": "اكتمل الترحيل: {n} ملف(ات) تم نقلها.",
        "no_match_search": "لا توجد ألعاب تطابق بحثك.",
    },
}

def T(key: str, **kwargs) -> str:
    s = STRINGS[LANG].get(key, STRINGS["en"].get(key, key))
    return s.format(**kwargs) if kwargs else s

def is_rtl() -> bool:
    return LANG == "ar"

def rtl_anchor() -> str:
    return "e" if is_rtl() else "w"

def rtl_side_main() -> str:
    return "right" if is_rtl() else "left"

def rtl_side_sec() -> str:
    return "left" if is_rtl() else "right"

def justify_rtl() -> str:
    return "right" if is_rtl() else "left"

class Theme:
    # Dark red theme – all colors defined here
    BG = "#050505"          # Main background
    BG2 = "#0A0A0A"
    SURFACE = "#111111"
    SURFACE2 = "#161616"
    SURFACE3 = "#1A1A1A"
    BORDER = "#2A0A0A"
    BORDER_HI = "#3A1010"
    ACCENT = "#FF1A1A"      # Primary red
    ACCENT_HOVER = "#FF3A3A"
    ACCENT_GLOW = "#FF2020"
    ACCENT_DIM = "#661111"
    DANGER = "#B30000"
    SUCCESS = "#C62828"
    WARNING = "#FF5555"
    TEXT = "#FFFFFF"
    TEXT_SUB = "#CCCCCC"
    TEXT_MUTED = "#888888"
    DISABLED = "#555555"
    INFO = "#38bdf8"        # Light blue for informational messages
    ERROR = "#ef4444"       # Red for errors

FONT_UI = "Segoe UI"
FONT_CODE = "Consolas"

FONT_TITLE = (FONT_UI, 17, "bold")
FONT_BODY = (FONT_UI, 12)
FONT_BOLD = (FONT_UI, 12, "bold")
FONT_SMALL = (FONT_UI, 10)
FONT_TINY = (FONT_UI, 9)
FONT_MONO = (FONT_CODE, 11)

STEAM_SEARCH_URL = "https://store.steampowered.com/api/storesearch/"
STEAM_APP_DETAILS_URL = "https://store.steampowered.com/api/appdetails/"
DOWNLOAD_BASE_R2 = "https://pub-5b6d3b7c03fd4ac1afb5bd3017850e20.r2.dev/"
DOWNLOAD_BASE_GITHUB = "https://codeload.github.com/SSMGAlt/ManifestHub2/zip/refs/heads/"
CHUNK_SIZE = 65536

def _base_dir() -> str:
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

SCRIPT_DIR = _base_dir()
os.chdir(SCRIPT_DIR)

def _get(url: str, timeout: int = 12) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": f"{APP_TITLE}/{APP_VERSION}"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()

def search_steam(query: str, limit: int = 15) -> list[dict]:
    params = urllib.parse.urlencode({"term": query, "l": "english", "cc": "US", "infinite": 1, "count": limit})
    data = json.loads(_get(f"{STEAM_SEARCH_URL}?{params}"))
    return [
        {"id": item.get("id"), "name": item.get("name", "Unknown"), "type": item.get("type", "unknown")}
        for item in data.get("items", [])
    ]

def fetch_game_name(app_id: str) -> str | None:
    try:
        data = json.loads(_get(f"{STEAM_APP_DETAILS_URL}?appids={app_id}"))
        app_data = data.get(str(app_id))
        if app_data and app_data.get("success"):
            return app_data["data"]["name"]
    except Exception:
        pass
    return None

def clean_game_name(name: str) -> str:
    name = re.sub(r'\b([A-Za-z])\.(?=[A-Za-z]\.)', r'\1', name)
    name = re.sub(r'\b([A-Za-z])\.$', r'\1', name)
    name = re.sub(r'(?<=[A-Za-z])\.(?=[A-Za-z])', '', name)
    name = re.sub(r'([a-z])([A-Z])', r'\1 \2', name)
    name = re.sub(r'([A-Z]+)([A-Z][a-z])', r'\1 \2', name)
    name = re.sub(r'[\-_:]+', ' ', name)
    name = re.sub(r"[^\w\s]", '', name)
    name = re.sub(r'_', ' ', name)
    name = re.sub(r' {2,}', ' ', name).strip()
    return name

def human_size(n: int | float) -> str:
    for unit in ("B", "KB", "MB", "GB"):
        if n < 1024:
            return f"{n:.1f} {unit}"
        n /= 1024
    return f"{n:.1f} TB"

def human_speed(bps: float) -> str:
    return human_size(int(bps)) + "/s"

def get_steam_path_registry() -> str | None:
    for subkey in [r"SOFTWARE\WOW6432Node\Valve\Steam", r"SOFTWARE\Valve\Steam"]:
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, subkey)
            path = winreg.QueryValueEx(key, "InstallPath")[0]
            winreg.CloseKey(key)
            return path
        except OSError:
            continue
    return None

def get_steam_path_scan() -> str | None:
    for drive in [f"{chr(d)}:\\" for d in range(ord('C'), ord('Z') + 1)]:
        for fragment in [("Program Files (x86)", "Steam"), ("Program Files", "Steam"), ("Steam",)]:
            path = os.path.join(drive, *fragment)
            if os.path.exists(os.path.join(path, "Steam.exe")):
                return path
    return None

def get_best_steam_path() -> str | None:
    path = get_steam_path_registry()
    if path and os.path.exists(os.path.join(path, "Steam.exe")):
        return path
    return get_steam_path_scan()

def migrate_steam_files(steam_path: str) -> int:
    old_dir = os.path.join(steam_path, "config", "stplug-in")
    new_dir = os.path.join(steam_path, "config", "lua")
    if not os.path.isdir(old_dir):
        return 0
    os.makedirs(new_dir, exist_ok=True)
    moved = 0
    for fname in os.listdir(old_dir):
        if fname.endswith(".lua") and fname[:-4].isdigit():
            src = os.path.join(old_dir, fname)
            dst = os.path.join(new_dir, fname)
            if not os.path.exists(dst):
                try:
                    shutil.move(src, dst)
                    moved += 1
                except OSError:
                    pass
    try:
        if os.path.isdir(old_dir) and not os.listdir(old_dir):
            os.rmdir(old_dir)
    except OSError:
        pass
    return moved

def lua_find_lua_files(steam_path: str) -> list[str]:
    lua_dir = os.path.join(steam_path, "config", "lua")
    if not os.path.isdir(lua_dir):
        return []
    files = []
    for name in os.listdir(lua_dir):
        if name.endswith(".lua") and name.count(".") == 1 and name.lower() != "steamtools.lua":
            files.append(os.path.join(lua_dir, name))
    return files

def lua_patch_file(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    if any("-- LUATOOLS: UPDATES DISABLED!" in line for line in lines):
        return "skipped_disabled"
    if not any("addappid" in line.lower() for line in lines):
        return "skipped_no_appid"

    new_lines = []
    changed = False
    for line in lines:
        if line.strip().startswith("setManifestid") and not line.strip().startswith("--"):
            new_lines.append("--" + line)
            changed = True
        else:
            new_lines.append(line)

    if changed:
        if not any("-- LUATOOLS: UPDATES DISABLED!" in line for line in new_lines):
            new_lines.insert(0, "-- LUATOOLS: UPDATES DISABLED!\n")
        with open(path, "w", encoding="utf-8") as f:
            f.writelines(new_lines)
        return "patched"
    return "already_patched"

def lua_unpatch_file(path: str) -> bool:
    try:
        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        new_lines = []
        changed = False
        marker = "-- LUATOOLS: UPDATES DISABLED!"
        for line in lines:
            stripped = line.lstrip()
            if stripped.startswith(marker):
                changed = True
                continue
            if stripped.startswith("--") and "setManifestid" in stripped:
                if line.startswith("--"):
                    new_line = line[2:]
                else:
                    new_line = line.replace("--", "", 1)
                new_lines.append(new_line)
                changed = True
            else:
                new_lines.append(line)
        if changed:
            with open(path, "w", encoding="utf-8") as f:
                f.writelines(new_lines)
            return True
        return False
    except Exception:
        return False

def lua_get_game_name(app_id: str, timeout: int = 10) -> str:
    try:
        data = json.loads(_get(f"https://store.steampowered.com/api/appdetails?appids={app_id}", timeout=timeout))
        if data.get(str(app_id), {}).get("success"):
            return data[str(app_id)]["data"].get("name", f"ID {app_id}")
    except Exception:
        pass
    return f"Unknown (ID {app_id})"

def remover_delete_game_files(steam_path: str, game_id: str) -> tuple[int, str]:
    log_text = f"--- AppID: {game_id} ---\n\n"
    files_deleted = 0

    lua_dir = os.path.join(steam_path, "config", "lua")
    lua_file = os.path.join(lua_dir, f"{game_id}.lua")
    log_text += f"Checking: {lua_file}\n"
    if os.path.isfile(lua_file):
        try:
            os.remove(lua_file)
            files_deleted += 1
            log_text += f"   Deleted: {lua_file}\n"
        except OSError as e:
            log_text += f"   ERROR deleting {lua_file}: {e}\n"
    else:
        log_text += "   No .lua file found.\n"

    depotcache_dir = os.path.join(steam_path, "config", "depotcache")
    log_text += f"\nChecking: {depotcache_dir}\n"
    if os.path.isdir(depotcache_dir):
        pattern = re.compile(rf"^{game_id}_\d+\.manifest$")
        found = False
        for filename in os.listdir(depotcache_dir):
            filepath = os.path.join(depotcache_dir, filename)
            if os.path.isfile(filepath) and pattern.match(filename):
                found = True
                try:
                    os.remove(filepath)
                    files_deleted += 1
                    log_text += f"   Deleted: {filename}\n"
                except OSError as e:
                    log_text += f"   ERROR deleting {filename}: {e}\n"
        if not found:
            log_text += "   No matching .manifest files found.\n"
    else:
        log_text += "   depotcache directory not found.\n"

    return files_deleted, log_text

class Tooltip:
    def __init__(self, widget, text: str):
        self._widget = widget
        self._text = text
        self._win: Toplevel | None = None
        widget.bind("<Enter>", self._show)
        widget.bind("<Leave>", self._hide)

    def _show(self, _event=None):
        try:
            x = self._widget.winfo_rootx() + self._widget.winfo_width() // 2
            y = self._widget.winfo_rooty() + self._widget.winfo_height() + 8
            self._win = Toplevel(self._widget)
            self._win.wm_overrideredirect(True)
            self._win.wm_geometry(f"+{x}+{y}")
            self._win.configure(bg=Theme.BORDER)
            outer = tk.Frame(self._win, bg=Theme.BORDER_HI, padx=1, pady=1)
            outer.pack()
            ctk.CTkLabel(
                outer, text=self._text,
                font=ctk.CTkFont(FONT_UI, 10),
                text_color=Theme.TEXT_SUB, fg_color=Theme.SURFACE2,
                corner_radius=6, padx=12, pady=6,
            ).pack()
        except Exception:
            pass

    def _hide(self, _event=None):
        if self._win:
            try:
                self._win.destroy()
            except Exception:
                pass
            self._win = None


class ContextMenu:
    def __init__(self, entry_widget: ctk.CTkEntry):
        self._entry = entry_widget
        self._menu = tk.Menu(
            entry_widget, tearoff=0,
            bg=Theme.SURFACE3, fg=Theme.TEXT,
            activebackground=Theme.BORDER_HI, activeforeground=Theme.TEXT,
            relief="flat", bd=0, font=(FONT_UI, 10),
        )
        self._menu.add_command(label="Copy",  command=self._do_copy)
        self._menu.add_command(label="Paste", command=self._do_paste)
        entry_widget.bind("<Button-3>", self._show)
        inner = self._get_inner(entry_widget)
        if inner:
            inner.bind("<Button-3>", self._show)

    @staticmethod
    def _get_inner(entry_widget: ctk.CTkEntry):
        if hasattr(entry_widget, "_entry"):
            return entry_widget._entry
        for child in entry_widget.winfo_children():
            if isinstance(child, tk.Entry):
                return child
        return None

    def _show(self, event):
        try:
            self._menu.tk_popup(event.x_root, event.y_root)
        finally:
            self._menu.grab_release()

    def _do_copy(self):
        inner = self._get_inner(self._entry)
        if not inner: return
        try:
            sel = inner.selection_get()
        except Exception:
            sel = inner.get()
        self._entry.clipboard_clear()
        self._entry.clipboard_append(sel)

    def _do_paste(self):
        inner = self._get_inner(self._entry)
        if not inner: return
        try:
            text = self._entry.clipboard_get()
        except Exception:
            return
        try:
            if inner.selection_present():
                inner.delete("sel.first", "sel.last")
        except Exception:
            pass
        inner.insert("insert", text)


class GlowDivider(ctk.CTkFrame):
    def __init__(self, parent, **kw):
        super().__init__(parent, height=2, fg_color=Theme.ACCENT_DIM,
                         corner_radius=0, **kw)


class SectionHeader(ctk.CTkFrame):
    def __init__(self, parent, text: str, top: int = 10, **kw):
        super().__init__(parent, fg_color="transparent", **kw)
        anchor = rtl_anchor()
        side_a = rtl_side_main()
        ctk.CTkLabel(
            self, text=text.upper() if not is_rtl() else text,
            font=ctk.CTkFont(FONT_UI, 10, "bold"),
            text_color=Theme.TEXT_MUTED,
            fg_color="transparent",
        ).pack(side=side_a, padx=(0, 8) if not is_rtl() else (8, 0))
        ctk.CTkFrame(self, height=1, fg_color=Theme.BORDER, corner_radius=0).pack(
            side=side_a, fill="x", expand=True, pady=(4, 0)
        )
        self.pack(fill="x", padx=18, pady=(top, 4))

def _make_entry(parent, placeholder: str = "", width: int = 0,
                height: int = 40, textvariable=None, **kw) -> ctk.CTkEntry:
    kwargs = dict(
        placeholder_text=placeholder,
        font=ctk.CTkFont(FONT_UI, 12),
        fg_color=Theme.SURFACE3,
        border_color=Theme.BORDER,
        border_width=1,
        text_color=Theme.TEXT,
        placeholder_text_color=Theme.TEXT_MUTED,
        height=height,
        corner_radius=8,
        justify="right" if is_rtl() else "left",
    )
    if textvariable is not None:
        kwargs["textvariable"] = textvariable
    if width:
        kwargs["width"] = width
    kwargs.update(kw)
    e = ctk.CTkEntry(parent, **kwargs)
    ContextMenu(e)
    return e

def _make_btn(parent, text: str, command=None, color: str = "accent",
              width: int = 0, height: int = 36, **kw) -> ctk.CTkButton:
    pairs = {
        "accent":  (Theme.ACCENT, Theme.ACCENT_HOVER),
        "green":   (Theme.SUCCESS, Theme.ACCENT_HOVER),
        "red":     (Theme.DANGER, Theme.ACCENT_HOVER),
        "purple":  (Theme.ACCENT, Theme.ACCENT_HOVER),
        "amber":   (Theme.WARNING, Theme.ACCENT_HOVER),
        "ghost":   (Theme.SURFACE3, Theme.SURFACE3),
        "dark":    (Theme.SURFACE2, Theme.SURFACE3),
    }
    fg, hov = pairs.get(color, (Theme.ACCENT, Theme.ACCENT_HOVER))
    kwargs = dict(
        text=text,
        font=ctk.CTkFont(FONT_UI, 11, "bold"),
        fg_color=fg, hover_color=hov,
        text_color=Theme.TEXT,
        corner_radius=8,
        height=height,
        command=command or (lambda: None),
    )
    if width:
        kwargs["width"] = width
    kwargs.update(kw)
    return ctk.CTkButton(parent, **kwargs)

class SafeToplevel(ctk.CTkToplevel):
    def __init__(self, parent, **kw):
        super().__init__(parent, **kw)
        self._closed = False
        self.configure(fg_color=Theme.BG)

    def destroy(self):
        self._closed = True
        try:
            super().destroy()
        except Exception:
            pass

    def _safe_after(self, ms: int, func, *args, **kwargs):
        def wrapper():
            if not self._closed:
                try:
                    func(*args, **kwargs)
                except Exception:
                    pass
        try:
            return self.after(ms, wrapper)
        except Exception:
            return None

    def _safe_update_widget(self, widget, attr: str, value):
        if self._closed:
            return
        try:
            if widget and widget.winfo_exists():
                if attr == "text":
                    widget.configure(text=value)
                elif attr == "text_color":
                    widget.configure(text_color=value)
                elif attr == "state":
                    widget.configure(state=value)
                elif attr == "fg_color":
                    widget.configure(fg_color=value)
                elif attr == "progress_color":
                    widget.configure(progress_color=value)
        except Exception:
            pass


class SearchDialog(SafeToplevel):
    def __init__(self, parent, on_select):
        super().__init__(parent)
        self.title(T("search_dialog_title"))
        self.geometry("580x480")
        self.minsize(460, 360)
        self.resizable(True, True)
        self.on_select = on_select
        self.results: list[dict] = []
        self._build()
        self.grab_set()
        self.transient(parent)
        self._safe_after(80, self._entry.focus_set)

    def _build(self):
        hdr = ctk.CTkFrame(self, fg_color=Theme.SURFACE, corner_radius=0, height=56)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)
        ctk.CTkLabel(
            hdr, text="🔍  " + T("search_dialog_title"),
            font=ctk.CTkFont(FONT_UI, 16, "bold"), text_color=Theme.TEXT,
        ).pack(side=rtl_side_main(), padx=18, pady=14)
        GlowDivider(hdr).pack(side="bottom", fill="x")

        bar = ctk.CTkFrame(self, fg_color=Theme.SURFACE2, corner_radius=0)
        bar.pack(fill="x")
        self._entry = _make_entry(bar, placeholder=T("search_placeholder"), height=42)
        self._entry.pack(side=rtl_side_main(), fill="x", expand=True,
                         padx=(14, 8) if not is_rtl() else (8, 14), pady=10)
        self._entry.bind("<Return>", lambda _: self._search())

        self._search_btn = _make_btn(bar, T("search_btn"), command=self._search,
                                     color="accent", width=100, height=38)
        self._search_btn.pack(side=rtl_side_main(), padx=(0, 14) if not is_rtl() else (14, 0), pady=10)

        self._status = ctk.CTkLabel(
            self, text="", height=22,
            font=ctk.CTkFont(FONT_UI, 10), text_color=Theme.TEXT_MUTED,
            fg_color=Theme.BG, anchor=rtl_anchor(),
        )
        self._status.pack(fill="x", padx=16, pady=(4, 2))

        lf = ctk.CTkFrame(self, fg_color=Theme.SURFACE2,
                          border_color=Theme.BORDER, border_width=1, corner_radius=10)
        lf.pack(fill="both", expand=True, padx=14, pady=(0, 6))

        sb = Scrollbar(lf, bg=Theme.SURFACE3, troughcolor=Theme.SURFACE2,
                       activebackground=Theme.ACCENT_DIM, relief="flat", bd=0, width=6)
        sb.pack(side="right", fill="y", padx=(0, 2), pady=4)

        self._lb = Listbox(
            lf, yscrollcommand=sb.set, selectmode=SINGLE,
            font=FONT_MONO, bg=Theme.SURFACE2, fg=Theme.TEXT,
            selectbackground=Theme.ACCENT_DIM, selectforeground="#fff",
            activestyle="none", relief="flat", borderwidth=0, highlightthickness=0,
        )
        self._lb.pack(side="left", fill="both", expand=True, padx=6, pady=6)
        self._lb.bind("<Double-Button-1>", lambda _: self._select())
        sb.config(command=self._lb.yview)

        ftr = ctk.CTkFrame(self, fg_color=Theme.SURFACE2, corner_radius=0, height=60)
        ftr.pack(fill="x", side="bottom")
        ftr.pack_propagate(False)

        _make_btn(ftr, T("cancel"), command=self.destroy,
                  color="dark", width=100, height=36).pack(
            side=rtl_side_sec(), padx=14, pady=12)
        _make_btn(ftr, T("select_game"), command=self._select,
                  color="green", width=150, height=36).pack(
            side=rtl_side_sec(), padx=(0, 6) if not is_rtl() else (6, 0), pady=12)

    def _set_status(self, msg: str, color: str = Theme.TEXT_MUTED):
        if not self._closed:
            try:
                self._status.configure(text=msg, text_color=color)
            except Exception:
                pass

    def _search(self):
        if self._closed:
            return
        q = self._entry.get().strip()
        if not q:
            self._set_status("  Please enter a game name." if LANG == "en"
                             else "  الرجاء إدخال اسم اللعبة.", Theme.WARNING)
            return
        self._set_status(T("searching"))
        self._search_btn.configure(state="disabled", text="...")
        self._lb.delete(0, END)
        self.results = []
        threading.Thread(target=self._worker, args=(q,), daemon=True).start()

    def _worker(self, q: str):
        if self._closed:
            return
        try:
            res = search_steam(q)
            self._safe_after(0, self._populate, res)
        except Exception as e:
            self._safe_after(0, lambda: self._set_status(f"Error: {e}", Theme.ERROR))
            self._safe_after(0, lambda: self._search_btn.configure(state="normal", text=T("search_btn")))

    _ICONS = {"app": "🎮", "dlc": "📦", "demo": "🎯", "music": "🎵"}

    def _populate(self, results: list[dict]):
        if self._closed:
            return
        self.results = results
        self._lb.delete(0, END)
        if not results:
            msg = "  No results found." if LANG == "en" else "  لا توجد نتائج."
            self._lb.insert(END, msg)
            self._lb.itemconfig(0, fg=Theme.TEXT_MUTED)
            self._set_status(msg.strip(), Theme.TEXT_MUTED)
        else:
            for i, r in enumerate(results, 1):
                icon = self._ICONS.get(r["type"], "▸")
                self._lb.insert(END, f"  {i:>2}.  {icon}  [{r['id']}]  {r['name']}")
            self._lb.selection_set(0)
            msg = (f"Found {len(results)} result(s). Double-click or press Select."
                   if LANG == "en"
                   else f"تم العثور على {len(results)} نتيجة. انقر مزدوجاً أو اختر.")
            self._set_status(msg, Theme.SUCCESS)
        self._search_btn.configure(state="normal", text=T("search_btn"))

    def _select(self):
        if self._closed:
            return
        sel = self._lb.curselection()
        if not sel or sel[0] >= len(self.results):
            msg = "  Select a game first." if LANG == "en" else "  اختر لعبة أولاً."
            self._set_status(msg, Theme.WARNING)
            return
        r = self.results[sel[0]]
        self.on_select(r["id"], r["name"])
        self.destroy()


class RemoveGameDialog(SafeToplevel):
    def __init__(self, parent, steam_path: str, on_done_callback):
        super().__init__(parent)
        self.title(T("remove_game_title"))
        self.geometry("500x420")
        self.minsize(420, 340)
        self.resizable(True, True)
        self.grab_set()
        self.transient(parent)
        self._steam_path = steam_path
        self._on_done = on_done_callback
        self._all_games: list[dict] = []
        self._filtered_games: list[dict] = []
        self._build()
        self._safe_after(100, self._scan_installed)

    def _build(self):
        hdr = ctk.CTkFrame(self, fg_color=Theme.SURFACE, corner_radius=0, height=56)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)
        ctk.CTkLabel(
            hdr, text="🗑  " + T("remove_game_title"),
            font=ctk.CTkFont(FONT_UI, 16, "bold"), text_color=Theme.TEXT,
        ).pack(side=rtl_side_main(), padx=18, pady=14)
        GlowDivider(hdr).pack(side="bottom", fill="x")

        bar = ctk.CTkFrame(self, fg_color=Theme.SURFACE2, corner_radius=0)
        bar.pack(fill="x")
        self._search_var = StringVar()
        self._search_var.trace_add("write", lambda *_: self._filter_list())
        self._entry = _make_entry(bar, placeholder=T("filter_placeholder"),
                                  height=40, textvariable=self._search_var)
        self._entry.pack(fill="x", padx=14, pady=10)

        self._status = ctk.CTkLabel(
            self, text=T("scanning"), height=22,
            font=ctk.CTkFont(FONT_UI, 10), text_color=Theme.TEXT_MUTED,
            fg_color=Theme.BG, anchor=rtl_anchor(),
        )
        self._status.pack(fill="x", padx=16, pady=(2, 2))

        lf = ctk.CTkFrame(self, fg_color=Theme.SURFACE2,
                          border_color=Theme.BORDER, border_width=1, corner_radius=10)
        lf.pack(fill="both", expand=True, padx=14, pady=(0, 6))

        sb = Scrollbar(lf, bg=Theme.SURFACE3, troughcolor=Theme.SURFACE2,
                       activebackground=Theme.ACCENT_DIM, relief="flat", bd=0, width=6)
        sb.pack(side="right", fill="y", padx=(0, 2), pady=4)

        self._lb = Listbox(
            lf, yscrollcommand=sb.set, selectmode=SINGLE,
            font=FONT_MONO, bg=Theme.SURFACE2, fg=Theme.TEXT,
            selectbackground=Theme.DANGER, selectforeground=Theme.TEXT,
            activestyle="none", relief="flat", borderwidth=0, highlightthickness=0,
        )
        self._lb.pack(side="left", fill="both", expand=True, padx=6, pady=6)
        self._lb.bind("<Double-Button-1>", lambda _: self._confirm_delete())
        self._lb.bind("<<ListboxSelect>>", lambda _: self._on_select())
        sb.config(command=self._lb.yview)

        ftr = ctk.CTkFrame(self, fg_color=Theme.SURFACE2, corner_radius=0, height=60)
        ftr.pack(fill="x", side="bottom")
        ftr.pack_propagate(False)

        _make_btn(ftr, T("cancel"), command=self.destroy,
                  color="dark", width=100, height=36).pack(
            side=rtl_side_sec(), padx=14, pady=12)

        self._delete_btn = _make_btn(ftr, T("btn_remove_game"), command=self._confirm_delete,
                                     color="red", width=160, height=36)
        self._delete_btn.pack(side=rtl_side_sec(), padx=(0, 6) if not is_rtl() else (6, 0), pady=12)
        self._delete_btn.configure(state="disabled")

    def _set_status(self, msg: str, color: str = Theme.TEXT_MUTED):
        if not self._closed:
            try:
                self._status.configure(text=msg, text_color=color)
            except Exception:
                pass

    def _on_select(self):
        if not self._closed:
            self._delete_btn.configure(state="normal" if self._lb.curselection() else "disabled")

    def _scan_installed(self):
        if self._closed:
            return
        lua_dir = os.path.join(self._steam_path, "config", "lua")
        if not os.path.isdir(lua_dir):
            self._set_status("config\\lua folder not found.", Theme.WARNING)
            return
        lua_files = [f for f in os.listdir(lua_dir) if f.endswith(".lua") and f[:-4].isdigit()]
        if not lua_files:
            self._set_status("No installed games found in config\\lua.", Theme.TEXT_MUTED)
            return
        msg = f"Loading {len(lua_files)} game(s)..." if LANG == "en" else f"جاري تحميل {len(lua_files)} لعبة..."
        self._set_status(msg, Theme.TEXT_MUTED)
        threading.Thread(target=self._resolve_names, args=(lua_dir, lua_files), daemon=True).start()

    def _resolve_names(self, lua_dir: str, lua_files: list[str]):
        if self._closed:
            return
        games = []
        for filename in sorted(lua_files, key=lambda f: f[:-4]):
            app_id = filename[:-4]
            lua_path = os.path.join(lua_dir, filename)
            name = lua_get_game_name(app_id, timeout=6)
            games.append({"app_id": app_id, "name": name, "lua_path": lua_path})
            self._safe_after(0, lambda g=list(games): self._set_games(g))
        n = len(games)
        msg = (f"{n} game(s) installed. Select one to remove."
               if LANG == "en" else f"{n} لعبة مثبّتة. اختر لحذفها.")
        self._safe_after(0, lambda: self._set_status(msg, Theme.SUCCESS))

    def _set_games(self, games: list[dict]):
        if self._closed:
            return
        self._all_games = games
        self._filter_list()

    def _filter_list(self):
        if self._closed:
            return
        query = self._search_var.get().strip().lower()
        self._filtered_games = (
            [g for g in self._all_games if query in g["name"].lower() or query in g["app_id"]]
            if query else list(self._all_games)
        )
        self._lb.delete(0, END)
        for g in self._filtered_games:
            self._lb.insert(END, f"  [{g['app_id']:>7}]  {g['name']}")
        self._delete_btn.configure(state="disabled")

    def _confirm_delete(self):
        if self._closed:
            return
        sel = self._lb.curselection()
        if not sel:
            return
        game = self._filtered_games[sel[0]]
        game_label = f"{game['name']} (ID {game['app_id']})"

        if not messagebox.askyesno(
            T("confirm_removal"),
            T("confirm_removal_msg", label=game_label),
        ):
            return

        self._delete_btn.configure(state="disabled")
        self._entry.configure(state="disabled")
        msg = "Deleting files..." if LANG == "en" else "جاري الحذف..."
        self._set_status(msg, Theme.INFO)
        threading.Thread(
            target=self._delete_worker,
            args=(game["app_id"], game["lua_path"], game_label),
            daemon=True,
        ).start()

    def _delete_worker(self, app_id: str, lua_path: str, game_label: str):
        if self._closed:
            return
        log_text = f"--- {game_label} ---\n\n"
        files_deleted = 0
        if os.path.isfile(lua_path):
            try:
                os.remove(lua_path)
                files_deleted += 1
                log_text += f"   Deleted: {lua_path}\n"
            except OSError as e:
                log_text += f"   ERROR deleting {lua_path}: {e}\n"
        else:
            log_text += f"   .lua file not found: {lua_path}\n"
        extra_deleted, extra_log = remover_delete_game_files(self._steam_path, app_id)
        files_deleted += extra_deleted
        log_text += extra_log
        self._safe_after(0, lambda: self._on_done(app_id, game_label, files_deleted, log_text))
        self._safe_after(0, self.destroy)


class UpdateManagerDialog(SafeToplevel):
    def __init__(self, parent, steam_path: str):
        super().__init__(parent)
        self.title(T("update_manager_title"))
        self.geometry("740x580")
        self.minsize(620, 500)
        self.resizable(True, True)
        self.transient(parent)
        self.grab_set()

        self._steam_path = steam_path
        self._all_games: list[dict] = []
        self._displayed_games: list[dict] = []
        self._updating_all = False
        self._scanning = False
        self._need_rescan = False

        self._build()
        self._safe_after(100, self._start_scan)

    def _build(self):
        hdr = ctk.CTkFrame(self, fg_color=Theme.SURFACE, corner_radius=0, height=64)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)
        title_lbl = ctk.CTkLabel(
            hdr, text="⚙  " + T("update_manager_title"),
            font=ctk.CTkFont(FONT_UI, 18, "bold"), text_color=Theme.TEXT,
        )
        title_lbl.pack(side=rtl_side_main(), padx=18, pady=12)

        self._stats_frame = ctk.CTkFrame(hdr, fg_color="transparent")
        self._stats_frame.pack(side=rtl_side_sec(), padx=18, pady=12)

        self._total_lbl = ctk.CTkLabel(
            self._stats_frame, text="", font=ctk.CTkFont(FONT_UI, 11), text_color=Theme.TEXT_SUB
        )
        self._total_lbl.pack(side=rtl_side_main(), padx=(0, 12))

        self._avail_lbl = ctk.CTkLabel(
            self._stats_frame, text="", font=ctk.CTkFont(FONT_UI, 11), text_color=Theme.WARNING
        )
        self._avail_lbl.pack(side=rtl_side_main())

        GlowDivider(hdr).pack(side="bottom", fill="x")

        action_bar = ctk.CTkFrame(self, fg_color=Theme.SURFACE2, corner_radius=0, height=54)
        action_bar.pack(fill="x")
        action_bar.pack_propagate(False)

        self._update_all_btn = _make_btn(
            action_bar, T("update_all"), command=self._update_all,
            color="green", height=38, width=140
        )
        self._update_all_btn.pack(side=rtl_side_main(), padx=14, pady=8)
        Tooltip(self._update_all_btn, T("update_all_tooltip"))

        self._refresh_btn = _make_btn(
            action_bar, "🔄 Refresh", command=self.refresh,
            color="accent", height=38, width=120
        )
        self._refresh_btn.pack(side=rtl_side_main(), padx=8, pady=8)

        self._close_btn = _make_btn(
            action_bar, T("close"), command=self.destroy,
            color="dark", height=38, width=100
        )
        self._close_btn.pack(side=rtl_side_sec(), padx=14, pady=8)

        progress_frame = ctk.CTkFrame(self, fg_color=Theme.SURFACE2, corner_radius=0)
        progress_frame.pack(fill="x", padx=14, pady=(8, 2))

        self._progress_bar = ctk.CTkProgressBar(
            progress_frame, height=8, corner_radius=4,
            fg_color=Theme.SURFACE3, progress_color=Theme.ACCENT
        )
        self._progress_bar.pack(fill="x", padx=0, pady=(6, 2))
        self._progress_bar.set(0)

        self._status_lbl = ctk.CTkLabel(
            progress_frame, text="", font=ctk.CTkFont(FONT_UI, 10),
            text_color=Theme.TEXT_MUTED, anchor=rtl_anchor()
        )
        self._status_lbl.pack(fill="x", padx=0, pady=(2, 6))

        search_frame = ctk.CTkFrame(self, fg_color=Theme.SURFACE2, corner_radius=0)
        search_frame.pack(fill="x", padx=14, pady=(4, 2))
        self._search_var = StringVar()
        self._search_var.trace_add("write", lambda *_: self._filter_games())
        self._search_entry = _make_entry(
            search_frame, placeholder=T("search_games"),
            height=32, textvariable=self._search_var
        )
        self._search_entry.pack(fill="x", padx=0, pady=4)

        self._list_frame = ctk.CTkScrollableFrame(
            self, fg_color=Theme.SURFACE, border_color=Theme.BORDER, border_width=1,
            corner_radius=10
        )
        self._list_frame.pack(fill="both", expand=True, padx=14, pady=(6, 14))

        self._game_widgets: dict[str, dict] = {}

        self._placeholder = ctk.CTkLabel(
            self._list_frame, text=T("scanning_games"),
            font=ctk.CTkFont(FONT_UI, 14), text_color=Theme.TEXT_MUTED
        )
        self._placeholder.pack(pady=40)

    def refresh(self):
        if self._closed:
            return
        if self._scanning:
            self._need_rescan = True
            self._status_lbl.configure(text="Rescan requested...")
        else:
            self._start_scan()

    def _start_scan(self):
        if self._closed or self._scanning:
            return
        self._scanning = True
        self._refresh_btn.configure(state="disabled", text="Scanning...")
        self._status_lbl.configure(text=T("scanning_games"))
        try:
            self._progress_bar.configure(mode="indeterminate")
            self._progress_bar.start()
        except Exception:
            pass
        self._destroy_all_widgets()
        self._show_placeholder(T("scanning_games"))
        threading.Thread(target=self._scan_games, daemon=True).start()

    def _scan_games(self):
        if self._closed:
            return
        migrate_steam_files(self._steam_path)

        lua_files = lua_find_lua_files(self._steam_path)
        if not lua_files:
            self._safe_after(0, lambda: self._show_placeholder(T("no_games_found")))
            self._scanning = False
            self._safe_after(0, lambda: self._refresh_btn.configure(state="normal", text="🔄 Refresh"))
            try:
                self._safe_after(0, lambda: self._progress_bar.stop())
                self._safe_after(0, lambda: self._progress_bar.configure(mode="determinate"))
            except Exception:
                pass
            self._safe_after(0, lambda: self._status_lbl.configure(text=""))
            if self._need_rescan:
                self._need_rescan = False
                self._safe_after(100, self._start_scan)
            return

        self._safe_after(0, self._hide_placeholder)

        games = []
        for lua_path in lua_files:
            if self._closed:
                return
            app_id = os.path.basename(lua_path).replace(".lua", "")
            if not app_id.isdigit():
                continue
            name = lua_get_game_name(app_id, timeout=5)
            status = self._check_patch_status(lua_path)
            patched = (status in ("already_patched", "skipped_disabled"))
            games.append({
                "app_id": app_id,
                "name": name,
                "lua_path": lua_path,
                "patched": patched,
                "updating": False,
                "failed": False,
            })

        games.sort(key=lambda g: g["name"].lower())
        self._safe_after(0, lambda: self._set_games(games))
        self._scanning = False
        self._safe_after(0, lambda: self._refresh_btn.configure(state="normal", text="🔄 Refresh"))
        try:
            self._safe_after(0, lambda: self._progress_bar.stop())
            self._safe_after(0, lambda: self._progress_bar.configure(mode="determinate"))
        except Exception:
            pass
        self._safe_after(0, lambda: self._status_lbl.configure(text=""))
        if self._need_rescan:
            self._need_rescan = False
            self._safe_after(100, self._start_scan)

    def _check_patch_status(self, path: str) -> str:
        try:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            if "-- LUATOOLS: UPDATES DISABLED!" in content:
                return "already_patched"
            if "addappid" not in content.lower():
                return "skipped_no_appid"
            lines = content.splitlines()
            has_uncommented = any(
                line.strip().startswith("setManifestid") and not line.strip().startswith("--")
                for line in lines
            )
            if not has_uncommented:
                return "already_patched"
            return "update_available"
        except Exception:
            return "error"

    def _set_games(self, games: list[dict]):
        if self._closed:
            return
        self._all_games = games
        self._filter_games()
        self._update_stats()

    def _show_placeholder(self, text: str):
        if self._closed:
            return
        try:
            self._placeholder.configure(text=text)
            self._placeholder.pack(pady=40)
            self._destroy_all_widgets()
        except Exception:
            pass

    def _hide_placeholder(self):
        if self._closed:
            return
        try:
            self._placeholder.pack_forget()
        except Exception:
            pass

    def _destroy_all_widgets(self):
        if self._closed:
            return
        for widget_dict in self._game_widgets.values():
            for w in widget_dict.values():
                if isinstance(w, ctk.CTkBaseClass):
                    try:
                        w.destroy()
                    except Exception:
                        pass
        self._game_widgets.clear()

    def _filter_games(self):
        if self._closed:
            return
        query = self._search_var.get().strip().lower()
        if query:
            self._displayed_games = [
                g for g in self._all_games
                if query in g["name"].lower() or query in g["app_id"]
            ]
        else:
            self._displayed_games = self._all_games[:]

        self._destroy_all_widgets()
        self._hide_placeholder()

        if not self._displayed_games:
            if query:
                self._show_placeholder(T("no_match_search"))
            else:
                self._show_placeholder(T("no_games_found"))
            return

        for game in self._displayed_games:
            if self._closed:
                return
            try:
                frame = ctk.CTkFrame(self._list_frame, fg_color=Theme.SURFACE2, corner_radius=8)
                frame.pack(fill="x", padx=4, pady=4)

                info_frame = ctk.CTkFrame(frame, fg_color="transparent")
                info_frame.pack(side=rtl_side_main(), fill="both", expand=True, padx=10, pady=6)

                name_lbl = ctk.CTkLabel(
                    info_frame, text=game["name"],
                    font=ctk.CTkFont(FONT_UI, 13, "bold"), text_color=Theme.TEXT
                )
                name_lbl.pack(anchor=rtl_anchor())

                id_lbl = ctk.CTkLabel(
                    info_frame, text=f"ID: {game['app_id']}",
                    font=ctk.CTkFont(FONT_UI, 10), text_color=Theme.TEXT_SUB
                )
                id_lbl.pack(anchor=rtl_anchor())

                action_frame = ctk.CTkFrame(frame, fg_color="transparent")
                action_frame.pack(side=rtl_side_sec(), padx=10, pady=6)

                status_lbl = ctk.CTkLabel(
                    action_frame, text="",
                    font=ctk.CTkFont(FONT_UI, 10), text_color=Theme.TEXT_SUB
                )
                status_lbl.pack(side=rtl_side_main(), padx=(0, 8))

                enable_btn = _make_btn(
                    action_frame, T("update_language"),
                    command=lambda g=game: self._enable_game(g),
                    color="green", height=30, width=80
                )
                enable_btn.pack(side=rtl_side_main(), padx=2)
                Tooltip(enable_btn, T("update_btn_tooltip"))

                disable_btn = _make_btn(
                    action_frame, T("cancel_update"),
                    command=lambda g=game: self._disable_game(g),
                    color="red", height=30, width=80
                )
                disable_btn.pack(side=rtl_side_main(), padx=2)
                Tooltip(disable_btn, T("disable_btn_tooltip"))

                self._game_widgets[game["app_id"]] = {
                    "frame": frame,
                    "status_lbl": status_lbl,
                    "enable_btn": enable_btn,
                    "disable_btn": disable_btn,
                }

                self._update_game_ui(game)
            except Exception:
                pass

    def _update_game_ui(self, game: dict):
        if self._closed:
            return
        widgets = self._game_widgets.get(game["app_id"])
        if not widgets:
            return
        status_lbl = widgets["status_lbl"]
        enable_btn = widgets["enable_btn"]
        disable_btn = widgets["disable_btn"]

        try:
            if game.get("updating", False):
                status_lbl.configure(text=T("updating"), text_color=Theme.INFO)
                enable_btn.configure(state="disabled")
                disable_btn.configure(state="disabled")
            elif game.get("patched", False):
                status_lbl.configure(text=T("auto_update_on"), text_color=Theme.SUCCESS)
                enable_btn.configure(state="disabled")
                disable_btn.configure(state="normal")
            elif game.get("failed", False):
                status_lbl.configure(text=T("failed"), text_color=Theme.ERROR)
                enable_btn.configure(state="normal")
                disable_btn.configure(state="normal")
            else:
                status_lbl.configure(text=T("auto_update_off"), text_color=Theme.WARNING)
                enable_btn.configure(state="normal")
                disable_btn.configure(state="disabled")
        except Exception:
            pass

    def _enable_game(self, game: dict):
        if self._closed or game.get("updating"):
            return
        game["updating"] = True
        widgets = self._game_widgets.get(game["app_id"])
        if widgets:
            try:
                widgets["enable_btn"].configure(state="disabled")
                widgets["disable_btn"].configure(state="disabled")
                widgets["status_lbl"].configure(text=T("updating"), text_color=Theme.INFO)
            except Exception:
                pass

        def worker():
            if self._closed:
                return
            result = lua_patch_file(game["lua_path"])
            if result == "patched" or result == "already_patched":
                game["patched"] = True
                game["failed"] = False
                status = T("auto_update_on")
                color = Theme.SUCCESS
            else:
                game["failed"] = True
                status = T("failed")
                color = Theme.ERROR
            game["updating"] = False
            self._safe_after(0, lambda: self._after_update(game, status, color))

        threading.Thread(target=worker, daemon=True).start()

    def _disable_game(self, game: dict):
        if self._closed or game.get("updating"):
            return
        game["updating"] = True
        widgets = self._game_widgets.get(game["app_id"])
        if widgets:
            try:
                widgets["enable_btn"].configure(state="disabled")
                widgets["disable_btn"].configure(state="disabled")
                widgets["status_lbl"].configure(text=T("updating"), text_color=Theme.INFO)
            except Exception:
                pass

        def worker():
            if self._closed:
                return
            success = lua_unpatch_file(game["lua_path"])
            if success:
                game["patched"] = False
                game["failed"] = False
                status = T("auto_update_off")
                color = Theme.WARNING
            else:
                game["failed"] = True
                status = T("failed")
                color = Theme.ERROR
            game["updating"] = False
            self._safe_after(0, lambda: self._after_update(game, status, color))

        threading.Thread(target=worker, daemon=True).start()

    def _after_update(self, game: dict, status: str, color: str):
        if self._closed:
            return
        self._update_game_ui(game)
        self._update_stats()

    def _update_stats(self):
        if self._closed:
            return
        total = len(self._all_games)
        patched = sum(1 for g in self._all_games if g.get("patched", False))
        try:
            self._total_lbl.configure(text=T("total_games", n=total))
            self._avail_lbl.configure(text=f"Patched: {patched} | Unpatched: {total - patched}")
        except Exception:
            pass

    def _update_all(self):
        if self._closed or self._updating_all:
            return
        if not messagebox.askyesno(T("update_all_confirm"), T("update_all_msg")):
            return

        self._updating_all = True
        self._update_all_btn.configure(state="disabled", text="Patching...")
        self._close_btn.configure(state="disabled")

        self._progress_bar.set(0)
        self._status_lbl.configure(text="Starting...")

        def worker():
            if self._closed:
                return
            lua_files = lua_find_lua_files(self._steam_path)
            if not lua_files:
                self._safe_after(0, lambda: messagebox.showinfo("Done", "No .lua files found."))
                self._safe_after(0, self._update_all_done)
                return

            total = len(lua_files)
            patched_count = 0
            failed_count = 0
            for i, path in enumerate(lua_files, 1):
                if self._closed:
                    return
                app_id = os.path.basename(path).replace(".lua", "")
                self._safe_after(0, lambda c=i, t=total, a=app_id: self._status_lbl.configure(
                    text=f"Patching {c}/{t}: {a}.lua"
                ))
                self._safe_after(0, lambda p=i/total: self._progress_bar.set(p))
                result = lua_patch_file(path)
                if result in ("patched", "already_patched"):
                    patched_count += 1
                    for g in self._all_games:
                        if g["app_id"] == app_id:
                            g["patched"] = True
                            g["failed"] = False
                            break
                else:
                    failed_count += 1
                time.sleep(0.05)

            self._safe_after(0, lambda: self._update_all_done(patched_count, failed_count))

        threading.Thread(target=worker, daemon=True).start()

    def _update_all_done(self, patched_count=None, failed_count=None):
        if self._closed:
            return
        self._updating_all = False
        self._update_all_btn.configure(state="normal", text=T("update_all"))
        self._close_btn.configure(state="normal")
        self._status_lbl.configure(text="Update All complete.")
        self._progress_bar.set(1.0)
        for game in self._all_games:
            self._update_game_ui(game)
        self._update_stats()

        if patched_count is not None:
            msg = f"Patched {patched_count} file(s)."
            if failed_count:
                msg += f"\nFailed: {failed_count}"
            messagebox.showinfo(T("update_complete"), msg)


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title(f"{APP_TITLE}  v{APP_VERSION}")
        self.geometry("640x630")
        self.minsize(580, 600)
        self.configure(fg_color=Theme.BG)
        self.resizable(True, True)
        self._game_name = ""
        self._rem_steam_path: str | None = get_best_steam_path()
        self._migrated = False
        self._update_dialog = None
        self._build()
        self.after(500, self._migrate_old_files)

    def _switch_language(self):
        global LANG
        LANG = "ar" if LANG == "en" else "en"
        for w in self.winfo_children():
            w.destroy()
        self._game_name = ""
        for attr in ("_update_status_lbl", "_update_log"):
            if hasattr(self, attr):
                delattr(self, attr)
        self._build()

    def _build(self):
        self._build_titlebar()
        self._build_tabs()

    def _build_titlebar(self):
        bar = ctk.CTkFrame(self, fg_color=Theme.SURFACE, corner_radius=0, height=50)
        bar.pack(fill="x")
        bar.pack_propagate(False)

        left = ctk.CTkFrame(bar, fg_color="transparent")
        left.pack(side=rtl_side_main(), padx=12, pady=6)

        ctk.CTkLabel(
            left, text="⬇",
            font=ctk.CTkFont(FONT_UI, 24, "bold"),
            text_color=Theme.ACCENT, fg_color="transparent",
        ).pack(side=rtl_side_main(), padx=(0, 6) if not is_rtl() else (6, 0))

        title_group = ctk.CTkFrame(left, fg_color="transparent")
        title_group.pack(side=rtl_side_main())

        ctk.CTkLabel(
            title_group, text=APP_TITLE,
            font=ctk.CTkFont(FONT_UI, 16, "bold"),
            text_color=Theme.TEXT, fg_color="transparent",
        ).pack(anchor=rtl_anchor())

        ctk.CTkLabel(
            title_group, text=f"v{APP_VERSION}  •  by {APP_AUTHOR}",
            font=ctk.CTkFont(FONT_UI, 8),
            text_color=Theme.TEXT_MUTED, fg_color="transparent",
        ).pack(anchor=rtl_anchor())

        lang_btn = _make_btn(bar, T("btn_lang"), command=self._switch_language,
                             color="ghost", width=80, height=28)
        lang_btn.pack(side=rtl_side_sec(), padx=(0, 12) if not is_rtl() else (12, 0))

        GlowDivider(bar).pack(side="bottom", fill="x")

    def _build_tabs(self):
        self._tabs = ctk.CTkTabview(
            self,
            fg_color=Theme.SURFACE,
            segmented_button_fg_color=Theme.SURFACE2,
            segmented_button_selected_color=Theme.ACCENT_DIM,
            segmented_button_selected_hover_color=Theme.ACCENT,
            segmented_button_unselected_color=Theme.SURFACE2,
            segmented_button_unselected_hover_color=Theme.BORDER,
            text_color=Theme.TEXT,
            border_color=Theme.BORDER, border_width=1,
            corner_radius=10,
            height=50,
        )
        self._tabs.pack(fill="both", expand=True, padx=12, pady=(6, 12))

        self._tab_patcher_key = T("tab_patcher")
        self._tab_about_key = T("tab_about")
        self._tabs.add(self._tab_patcher_key)
        self._tabs.add(self._tab_about_key)

        self._build_patcher_tab(self._tabs.tab(self._tab_patcher_key))
        self._build_about_tab(self._tabs.tab(self._tab_about_key))

    def _build_patcher_tab(self, parent):
        scroll_frame = ctk.CTkScrollableFrame(parent, fg_color="transparent")
        scroll_frame.pack(fill="both", expand=True)

        SectionHeader(scroll_frame, T("section_appid"), top=4)
        id_row = ctk.CTkFrame(scroll_frame, fg_color="transparent")
        id_row.pack(fill="x", padx=14, pady=(0, 2))

        self._id_var = StringVar()
        self._id_var.trace_add("write", self._on_id_typed)

        self._id_entry = _make_entry(id_row, placeholder=T("id_placeholder"),
                                     width=150, height=34, textvariable=self._id_var,
                                     font=ctk.CTkFont(FONT_CODE, 12))
        self._id_entry.pack(side=rtl_side_main(), padx=(0, 8) if not is_rtl() else (8, 0))

        self._name_lbl = ctk.CTkLabel(
            id_row, text="",
            font=ctk.CTkFont(FONT_UI, 10), text_color=Theme.SUCCESS,
            fg_color="transparent",
        )
        self._name_lbl.pack(side=rtl_side_main(), fill="x", expand=True)

        self._rem_all_btn = _make_btn(
            id_row, T("btn_remove_all"), command=self._rem_remove_all_games,
            color="red", height=34,
        )
        self._rem_all_btn.pack(side=rtl_side_sec())
        Tooltip(self._rem_all_btn, T("tip_remove_all"))

        SectionHeader(scroll_frame, T("section_actions"), top=4)

        row1 = ctk.CTkFrame(scroll_frame, fg_color="transparent")
        row1.pack(fill="x", padx=14, pady=(0, 4))

        self._search_btn = _make_btn(row1, T("btn_search"), command=self._open_search,
                                     color="accent", height=34)
        self._search_btn.pack(side=rtl_side_main(), fill="x", expand=True, padx=(0, 4) if not is_rtl() else (4, 0))
        Tooltip(self._search_btn, T("tip_search"))

        self._dl_btn = _make_btn(row1, T("btn_download"), command=self._start_download,
                                 color="green", height=34)
        self._dl_btn.pack(side=rtl_side_main(), fill="x", expand=True, padx=(0, 4) if not is_rtl() else (4, 0))
        Tooltip(self._dl_btn, T("tip_download"))

        self._online_fix_btn = _make_btn(row1, T("btn_online_fix"), command=self._open_online_fix,
                                         color="purple", height=34)
        self._online_fix_btn.pack(side=rtl_side_main(), fill="x", expand=True, padx=(0, 4) if not is_rtl() else (4, 0))
        Tooltip(self._online_fix_btn, T("tip_online_fix"))

        self._update_btn = _make_btn(row1, T("btn_update"), command=self._open_update_manager,
                                     color="accent", height=34)
        self._update_btn.pack(side=rtl_side_main(), fill="x", expand=True)
        Tooltip(self._update_btn, T("tip_update"))

        row2 = ctk.CTkFrame(scroll_frame, fg_color="transparent")
        row2.pack(fill="x", padx=14, pady=(0, 2))

        self._rem_folder_btn = _make_btn(row2, T("btn_steam_folder"), command=self._rem_change_path,
                                         color="ghost", height=30)
        self._rem_folder_btn.pack(side=rtl_side_main(), fill="x", expand=True, padx=(0, 4) if not is_rtl() else (4, 0))
        Tooltip(self._rem_folder_btn, T("tip_steam_folder"))

        self._rem_delete_btn = _make_btn(row2, T("btn_remove_game"), command=self._rem_remove_game,
                                         color="red", height=30)
        self._rem_delete_btn.pack(side=rtl_side_main(), fill="x", expand=True, padx=(0, 4) if not is_rtl() else (4, 0))
        Tooltip(self._rem_delete_btn, T("tip_remove_game"))

        self._rem_restart_btn = _make_btn(
            row2, T("btn_restart_steam"),
            command=lambda: threading.Thread(target=self._rem_restart_steam, daemon=True).start(),
            color="green", height=30,
        )
        self._rem_restart_btn.pack(side=rtl_side_main(), fill="x", expand=True, padx=(0, 4) if not is_rtl() else (4, 0))
        Tooltip(self._rem_restart_btn, T("tip_restart_steam"))

        self._fix_steamtools_btn = _make_btn(row2, T("btn_fix_steamtools"),
                                             command=self._fix_steamtools,
                                             color="amber", height=30,
                                             text_color="#000000")
        self._fix_steamtools_btn.pack(side=rtl_side_main(), fill="x", expand=True)
        Tooltip(self._fix_steamtools_btn, T("tip_fix_steamtools"))

        row3 = ctk.CTkFrame(scroll_frame, fg_color="transparent")
        row3.pack(fill="x", padx=14, pady=(0, 2))

        self._steamtools_dl_btn = _make_btn(
            row3, T("btn_dl_steamtools"),
            command=self._download_and_run_steamtools,
            color="accent", height=30,
        )
        self._steamtools_dl_btn.pack(side=rtl_side_main(), fill="x", expand=True, padx=(0, 4) if not is_rtl() else (4, 0))
        Tooltip(self._steamtools_dl_btn, T("tip_dl_steamtools"))

        self._steamtools_run_btn = _make_btn(row3, T("btn_run_steamtools"),
                                             command=self._run_steamtools,
                                             color="green", height=30)
        self._steamtools_run_btn.pack(side=rtl_side_main(), fill="x", expand=True)
        Tooltip(self._steamtools_run_btn, "Launch SteamTools")

        self._rem_path_lbl = ctk.CTkLabel(
            scroll_frame, text="", font=ctk.CTkFont(FONT_UI, 8),
            text_color=Theme.TEXT_MUTED, fg_color="transparent", anchor=rtl_anchor(),
        )
        self._rem_path_lbl.pack(anchor=rtl_anchor(), padx=16, pady=(2, 0))
        self._rem_update_path_label()

        SectionHeader(scroll_frame, T("section_password"), top=2)
        pw_row = ctk.CTkFrame(scroll_frame, fg_color="transparent")
        pw_row.pack(fill="x", padx=14, pady=(0, 2))

        self._pw_entry = ctk.CTkEntry(
            pw_row, font=ctk.CTkFont(FONT_CODE, 11),
            fg_color=Theme.SURFACE3, border_color=Theme.BORDER,
            border_width=1, text_color=Theme.TEXT,
            height=32, corner_radius=8,
            justify="right" if is_rtl() else "left",
        )
        self._pw_entry.insert(0, T("pw_label"))
        self._pw_entry.configure(state="readonly")
        self._pw_entry.pack(side=rtl_side_main(), fill="x", expand=True,
                            padx=(0, 6) if not is_rtl() else (6, 0))

        self._pw_copy_btn = _make_btn(pw_row, T("btn_copy"), command=self._copy_password,
                                      color="ghost", width=90, height=32)
        self._pw_copy_btn.pack(side=rtl_side_main())
        Tooltip(self._pw_copy_btn, T("tip_copy_pw"))

        SectionHeader(scroll_frame, T("section_progress"), top=2)
        self._progress = ctk.CTkProgressBar(
            scroll_frame, height=6, corner_radius=3,
            fg_color=Theme.SURFACE3, progress_color=Theme.ACCENT,
        )
        self._progress.pack(fill="x", padx=14, pady=(0, 2))
        self._progress.set(0)

        self._dl_lbl = ctk.CTkLabel(
            scroll_frame, text=T("idle"),
            font=ctk.CTkFont(FONT_UI, 9), text_color=Theme.TEXT_MUTED,
            fg_color="transparent", anchor=rtl_anchor(),
        )
        self._dl_lbl.pack(anchor=rtl_anchor(), padx=16, pady=(1, 0))

        SectionHeader(scroll_frame, T("section_log"), top=2)
        log_card = ctk.CTkFrame(
            scroll_frame, fg_color=Theme.SURFACE2,
            border_color=Theme.BORDER, border_width=1, corner_radius=8,
        )
        log_card.pack(fill="both", expand=True, padx=14, pady=(0, 10))

        self._log_box = ctk.CTkTextbox(
            log_card, corner_radius=0,
            fg_color="transparent",
            font=ctk.CTkFont(FONT_CODE, 9),
            text_color=Theme.TEXT_SUB,
            scrollbar_button_color=Theme.SURFACE3,
            scrollbar_button_hover_color=Theme.BORDER,
            wrap="none",
        )
        self._log_box.pack(fill="both", expand=True, padx=4, pady=(4, 0))
        self._log_box.configure(state="disabled")

        _make_btn(log_card, T("btn_copy_log"), command=self._copy_log,
                  color="dark", width=90, height=22,
                  font=ctk.CTkFont(FONT_UI, 8)).pack(
            anchor=rtl_anchor(), padx=4, pady=(2, 4))

        self._log(T("log_ready"))

    def _build_about_tab(self, parent):
        hero = ctk.CTkFrame(parent, fg_color=Theme.SURFACE2,
                            border_color=Theme.BORDER_HI, border_width=1,
                            corner_radius=12)
        hero.pack(fill="x", padx=16, pady=(14, 0))

        ctk.CTkLabel(
            hero, text="⬇  " + APP_TITLE,
            font=ctk.CTkFont(FONT_UI, 20, "bold"),
            text_color=Theme.ACCENT, fg_color="transparent",
        ).pack(pady=(14, 2))

        ctk.CTkLabel(
            hero, text=T("about_version"),
            font=ctk.CTkFont(FONT_UI, 10),
            text_color=Theme.TEXT_MUTED, fg_color="transparent",
        ).pack(pady=(0, 12))

        GlowDivider(parent).pack(fill="x", padx=16, pady=10)

        info_card = ctk.CTkFrame(parent, fg_color=Theme.SURFACE2,
                                 border_color=Theme.BORDER, border_width=1, corner_radius=10)
        info_card.pack(fill="x", padx=16, pady=(0, 10))

        ctk.CTkLabel(
            info_card, text=T("about_info"),
            font=ctk.CTkFont(FONT_UI, 10),
            text_color=Theme.TEXT, justify=justify_rtl(), wraplength=480,
            fg_color="transparent",
        ).pack(padx=14, pady=12, anchor=rtl_anchor())

        tg_btn = _make_btn(parent, "✈  " + T("about_telegram"),
                           command=lambda: webbrowser.open("https://t.me/X2_616"),
                           color="accent", height=36)
        tg_btn.pack(fill="x", padx=16, pady=(0, 6))

        dc_btn = _make_btn(parent, "🎮  Discord Server",
                           command=lambda: webbrowser.open("https://discord.gg/btRCeujadA"),
                           height=36)
        dc_btn.configure(fg_color="#5865F2", hover_color="#7289DA", text_color="#ffffff")
        dc_btn.pack(fill="x", padx=16, pady=(0, 14))

    def _log(self, msg: str):
        try:
            ts = time.strftime("%H:%M:%S")
            self._log_box.configure(state="normal")
            self._log_box.insert(END, f"[{ts}] {msg}")
            self._log_box.see(END)
            self._log_box.configure(state="disabled")
        except Exception:
            pass

    def _set_dl_label(self, msg: str, color: str = Theme.TEXT_MUTED):
        try:
            self._dl_lbl.configure(text=msg, text_color=color)
        except Exception:
            pass

    def _on_id_typed(self, *_):
        self._game_name = ""
        try:
            self._name_lbl.configure(text="")
        except Exception:
            pass

    def _copy_password(self):
        self.clipboard_clear()
        self.clipboard_append(T("pw_label"))
        self._pw_copy_btn.configure(text=T("copied"))
        self.after(2000, lambda: self._pw_copy_btn.configure(text=T("btn_copy")))

    def _copy_log(self):
        try:
            self._log_box.configure(state="normal")
            content = self._log_box.get("1.0", END)
            self._log_box.configure(state="disabled")
            self.clipboard_clear()
            self.clipboard_append(content)
            self._set_dl_label(T("log_copied"), Theme.INFO)
            self.after(2500, lambda: self._set_dl_label(T("idle")))
        except Exception:
            pass

    def _open_search(self):
        SearchDialog(self, self._on_game_selected)

    def _on_game_selected(self, app_id, name: str):
        self._id_var.set(str(app_id))
        self._game_name = clean_game_name(name)
        self._name_lbl.configure(text=self._game_name)
        self._log(f"Selected: {name} → {self._game_name} (ID {app_id})\n")

    def _ensure_game_name(self, app_id: str) -> bool:
        if self._game_name:
            return True
        fetching_msg = "Fetching game name..." if LANG == "en" else "جاري جلب اسم اللعبة..."
        self._set_dl_label(fetching_msg, Theme.INFO)
        self.update_idletasks()
        try:
            fetched = fetch_game_name(app_id)
        except Exception as exc:
            self._set_dl_label("  Failed to fetch game name.", Theme.ERROR)
            messagebox.showerror(T("error"), f"Error fetching game name:\n{exc}")
            return False
        if fetched:
            cleaned = clean_game_name(fetched)
            self._game_name = cleaned
            self._name_lbl.configure(text=cleaned)
            self._log(f"Fetched: {fetched} → {cleaned}\n")
            return True
        self._set_dl_label("")
        messagebox.showerror(
            "Game Not Found",
            f"Could not retrieve the game name for App ID {app_id}.\n"
            "Use 'Search Game' to select the game first.",
        )
        return False

    def _validate_app_id(self) -> str | None:
        app_id = self._id_var.get().strip()
        if not app_id:
            messagebox.showwarning(T("no_appid_warn"), T("no_appid_msg"))
            return None
        if not app_id.isdigit():
            messagebox.showerror(T("invalid_appid"), T("invalid_appid_msg"))
            return None
        return app_id

    def _migrate_old_files(self):
        if self._migrated or not self._rem_steam_path:
            return
        self._migrated = True
        self._log("Checking for old .lua files in stplug-in...\n")
        moved = migrate_steam_files(self._rem_steam_path)
        if moved:
            self._log(T("migrated", n=moved) + "\n")
        else:
            self._log("No old .lua files to migrate.\n")

    def _start_download(self):
        app_id = self._validate_app_id()
        if app_id is None:
            return
        if not self._ensure_game_name(app_id):
            self._log(f"Could not fetch game name for ID {app_id}.\n")

        if not self._rem_steam_path:
            messagebox.showerror(T("no_steam_folder"), T("no_steam_msg2"))
            return
        steam_path = self._rem_steam_path

        tmp_fd, tmp_zip = tempfile.mkstemp(suffix=".zip", prefix=f"x2dl_{app_id}_")
        os.close(tmp_fd)
        extract_temp = tempfile.mkdtemp(prefix=f"x2extract_{app_id}_")

        self._set_buttons(downloading=True)
        self._progress.configure(mode="indeterminate", progress_color=Theme.ACCENT)
        self._progress.start()
        self._log(f"Starting download for App ID {app_id}...\n")
        threading.Thread(target=self._dl_worker, args=(app_id, tmp_zip, extract_temp, steam_path), daemon=True).start()

    def _set_buttons(self, downloading: bool):
        state = "disabled" if downloading else "normal"
        dl_text = T("downloading") if downloading else T("btn_download")
        self._dl_btn.configure(state=state, text=dl_text)
        self._search_btn.configure(state=state)
        self._online_fix_btn.configure(state=state)
        self._update_btn.configure(state=state)

    def _r2_url_for(self, app_id: str) -> str:
        return f"{DOWNLOAD_BASE_R2}{app_id}.zip"

    def _github_url_for(self, app_id: str) -> str:
        return f"{DOWNLOAD_BASE_GITHUB}{app_id}"

    def _dl_worker(self, app_id: str, save_path: str, extract_dir: str, steam_path: str):
        def _fetch_stream(url: str, label: str) -> bool:
            req = urllib.request.Request(url, headers={
                "User-Agent": f"{APP_TITLE}/{APP_VERSION}", "Accept": "*/*"
            })
            with urllib.request.urlopen(req, timeout=30) as r:
                ct = (r.headers.get("Content-Type") or "").lower()
                clen = int(r.headers.get("Content-Length") or 0)
                if ("xml" in ct or "html" in ct) and (clen == 0 or clen < 512):
                    raise ValueError(f"Source {label}: unexpected content-type '{ct}'")
                total = clen or None
                if total:
                    self.after(0, lambda: self._progress.configure(mode="determinate"))
                downloaded, t0 = 0, time.time()
                with open(save_path, "wb") as f:
                    while True:
                        chunk = r.read(CHUNK_SIZE)
                        if not chunk:
                            break
                        f.write(chunk)
                        downloaded += len(chunk)
                        elapsed = max(time.time() - t0, 0.001)
                        spd = downloaded / elapsed
                        if total:
                            pct = downloaded / total
                            self.after(0, lambda p=pct: self._progress.set(p))
                            self.after(0, lambda d=downloaded, t=total, s=spd:
                                self._set_dl_label(
                                    f"  [{label}]  {human_size(d)} / {human_size(t)}  •  {human_speed(s)}"
                                ))
                        else:
                            self.after(0, lambda d=downloaded, s=spd:
                                self._set_dl_label(f"  [{label}]  {human_size(d)}  •  {human_speed(s)}"))
                if downloaded < 22:
                    raise ValueError(f"Source {label}: file too small ({downloaded} B)")
            return True

        def _try_source(url: str, label: str) -> tuple[bool, str]:
            try:
                self.after(0, lambda lbl=label: self._log(f"Trying source {lbl}: {url}\n"))
                self.after(0, lambda lbl=label: self._set_dl_label(f"  Trying {lbl}...", Theme.INFO))
                return _fetch_stream(url, label), ""
            except urllib.error.HTTPError as e:
                if e.code in (403, 404):
                    self.after(0, lambda c=e.code, lbl=label: self._log(f"Source {lbl}: HTTP {c} — not found\n"))
                    return False, ""
                self.after(0, lambda c=e.code, lbl=label: self._log(f"Source {lbl}: HTTP {c} — fallback\n"))
                return False, f"HTTP {e.code} ({e.reason})"
            except Exception as e:
                self.after(0, lambda err=e, lbl=label: self._log(f"Source {lbl}: {err} — fallback\n"))
                return False, str(e)

        try:
            ok, _err1 = _try_source(self._r2_url_for(app_id), "1 (R2 CDN)")
            if not ok:
                self.after(0, lambda: self._progress.configure(mode="indeterminate"))
                self.after(0, self._progress.start)
                ok, err2 = _try_source(self._github_url_for(app_id), "2 (GitHub)")
                if not ok:
                    self.after(0, lambda m=err2 or "File not found.": self._dl_done(False, save_path, extract_dir, steam_path, error=m))
                    return
            self.after(0, lambda: self._dl_done(True, save_path, extract_dir, steam_path))
        except Exception as exc:
            self.after(0, lambda e=exc: self._dl_done(False, save_path, extract_dir, steam_path, error=str(e)))

    def _dl_done(self, ok: bool, save_path: str, extract_dir: str, steam_path: str, *, error: str = ""):
        try:
            self._progress.stop()
        except Exception:
            pass
        self._progress.set(1.0 if ok else 0.0)
        self._progress.configure(
            mode="determinate",
            progress_color=Theme.SUCCESS if ok else Theme.ERROR,
        )
        self._set_buttons(downloading=False)
        if ok:
            self._set_dl_label(T("extracting"), Theme.INFO)
            self._log(f" Download complete. Extracting and moving files...\n")
            try:
                with zipfile.ZipFile(save_path, "r") as zf:
                    zf.extractall(extract_dir)

                lua_dir = os.path.join(steam_path, "config", "lua")
                depotcache_dir = os.path.join(steam_path, "config", "depotcache")
                os.makedirs(lua_dir, exist_ok=True)
                os.makedirs(depotcache_dir, exist_ok=True)

                moved_count = 0
                for root, _, files in os.walk(extract_dir):
                    for fname in files:
                        full_path = os.path.join(root, fname)
                        if fname.endswith(".lua"):
                            dest = os.path.join(lua_dir, fname)
                            shutil.move(full_path, dest)
                            moved_count += 1
                            self._log(f"  Moved {fname} -> config/lua/\n")
                        elif fname.endswith(".manifest"):
                            dest = os.path.join(depotcache_dir, fname)
                            shutil.move(full_path, dest)
                            moved_count += 1
                            self._log(f"  Moved {fname} -> config/depotcache/\n")

                self._log(f"  Moved {moved_count} files to Steam folders.\n")
                self._set_dl_label(T("done_opened"), Theme.SUCCESS)
                messagebox.showinfo(T("dl_ok_title"), T("dl_ok_msg"))
            except Exception as exc:
                self._set_dl_label("  Extraction or move failed.", Theme.ERROR)
                self._log(f" Error: {exc}\n")
                messagebox.showerror(T("extract_fail"), T("extract_fail_msg", err=exc))
            finally:
                try:
                    os.remove(save_path)
                except OSError:
                    pass
                try:
                    shutil.rmtree(extract_dir, ignore_errors=True)
                except OSError:
                    pass
        else:
            try:
                os.remove(save_path)
            except OSError:
                pass
            try:
                shutil.rmtree(extract_dir, ignore_errors=True)
            except OSError:
                pass
            msg = error or "File not found on R2 CDN or GitHub."
            self._set_dl_label(T("dl_failed_lbl"), Theme.ERROR)
            self._log(f" Failed: {msg}\n")
            messagebox.showerror(T("dl_fail_title"),
                f"Could not download the file.\n\nBoth R2 CDN and GitHub were tried.\n\nDetails: {msg}")

    def _open_online_fix(self):
        app_id = self._validate_app_id()
        if app_id is None:
            return
        if not self._ensure_game_name(app_id):
            return
        encoded = urllib.parse.quote(self._game_name, safe="")
        url = f"https://online-fix.me/index.php?do=search&subaction=search&story={encoded}"
        self._log(f" Opening Online Fix: {self._game_name}\n   {url}\n")
        webbrowser.open(url)
        self._set_dl_label(f"  Opened Online Fix: {self._game_name}")

    def _open_update_manager(self):
        if not self._rem_steam_path:
            messagebox.showerror(T("no_steam_folder"), T("no_steam_msg2"))
            return
        self._migrate_old_files()

        if self._update_dialog is not None and self._update_dialog.winfo_exists():
            self._update_dialog.refresh()
            self._update_dialog.lift()
        else:
            self._update_dialog = UpdateManagerDialog(self, self._rem_steam_path)
            self._update_dialog.bind("<Destroy>", lambda e: self._on_update_dialog_closed())

    def _on_update_dialog_closed(self):
        self._update_dialog = None

    def _fix_steamtools(self):
        if not self._rem_steam_path:
            messagebox.showerror(T("no_steam_folder"), T("no_steam_msg2"))
            return
        steam_path = self._rem_steam_path

        url = "https://github.com/OpenSteam001/OpenSteamTool/releases/download/1.4.8/OpenSteamTool-1.4.8-Release.zip"
        self._log(f"Downloading OpenSteamTool from {url}\n")
        self._fix_steamtools_btn.configure(state="disabled", text="Downloading...")

        def worker():
            temp_dir = tempfile.mkdtemp(prefix="opensteamtool_")
            zip_path = os.path.join(temp_dir, "OpenSteamTool.zip")
            try:
                req = urllib.request.Request(url, headers={"User-Agent": f"{APP_TITLE}/{APP_VERSION}"})
                with urllib.request.urlopen(req, timeout=30) as response:
                    total = int(response.headers.get("Content-Length", 0))
                    downloaded = 0
                    with open(zip_path, "wb") as f:
                        while True:
                            chunk = response.read(CHUNK_SIZE)
                            if not chunk:
                                break
                            f.write(chunk)
                            downloaded += len(chunk)
                            if total:
                                progress = downloaded / total
                                self.after(0, lambda p=progress: self._fix_steamtools_btn.configure(
                                    text=f"Downloading {int(p*100)}%"
                                ))
                            else:
                                self.after(0, lambda d=downloaded: self._log(f"  Downloaded {human_size(d)}\n"))
                if downloaded == 0:
                    raise Exception("Downloaded file is empty.")

                self.after(0, lambda: self._log("Download complete. Extracting DLLs...\n"))
                self.after(0, lambda: self._fix_steamtools_btn.configure(text="Extracting..."))

                with zipfile.ZipFile(zip_path, "r") as zf:
                    for member in zf.infolist():
                        if member.is_dir():
                            continue
                        if member.filename.lower().endswith(".dll"):
                            target = os.path.join(steam_path, os.path.basename(member.filename))
                            if not os.path.exists(target):
                                with zf.open(member) as src, open(target, "wb") as dst:
                                    dst.write(src.read())
                                self._log(f"  Placed {os.path.basename(member.filename)} in Steam folder.\n")
                            else:
                                self._log(f"  Skipped {os.path.basename(member.filename)} (already exists).\n")

                self.after(0, lambda: self._log("OpenSteamTool installed successfully.\n"))
                self.after(0, lambda: self._fix_steamtools_btn.configure(
                    state="normal", text=T("btn_fix_steamtools")
                ))
                self.after(0, lambda: messagebox.showinfo("Success", T("fix_st_done")))

            except Exception as e:
                self.after(0, lambda: self._log(f"Error: {e}\n"))
                self.after(0, lambda: self._fix_steamtools_btn.configure(
                    state="normal", text=T("btn_fix_steamtools")
                ))
                self.after(0, lambda: messagebox.showerror(T("error"), f"{T('installer_download_failed')}\n{e}"))
            finally:
                try:
                    shutil.rmtree(temp_dir, ignore_errors=True)
                except OSError:
                    pass

        threading.Thread(target=worker, daemon=True).start()

    def _download_and_run_steamtools(self):
        url = "https://steamtools.net/res/st-setup-1.8.30.exe"
        self._download_and_run_installer(url, T("btn_dl_steamtools"), self._steamtools_dl_btn)

    def _download_and_run_installer(self, url: str, success_message: str, button_ref):
        button_ref.configure(state="disabled", text="Downloading...")
        self._log(f"Downloading installer from {url}\n")

        def worker():
            temp_dir = tempfile.gettempdir()
            filename = os.path.basename(url).split('?')[0] or "installer.exe"
            exe_path = os.path.join(temp_dir, filename)

            try:
                req = urllib.request.Request(url, headers={"User-Agent": f"{APP_TITLE}/{APP_VERSION}"})
                with urllib.request.urlopen(req, timeout=30) as response:
                    total = int(response.headers.get("Content-Length", 0))
                    downloaded = 0
                    with open(exe_path, "wb") as f:
                        while True:
                            chunk = response.read(CHUNK_SIZE)
                            if not chunk:
                                break
                            f.write(chunk)
                            downloaded += len(chunk)
                            if total:
                                progress = downloaded / total
                                self.after(0, lambda p=progress: button_ref.configure(
                                    text=f"Downloading {int(p*100)}%"
                                ))
                            else:
                                self.after(0, lambda d=downloaded: self._log(f"  Downloaded {human_size(d)}\n"))
                if downloaded == 0:
                    raise Exception("Downloaded file is empty.")

                self.after(0, lambda: self._log("Download complete. Launching installer...\n"))
                self.after(0, lambda: button_ref.configure(text="Launching..."))

                subprocess.Popen([exe_path], shell=True)

                def delete_later():
                    time.sleep(5)
                    try:
                        os.remove(exe_path)
                    except OSError:
                        pass
                threading.Thread(target=delete_later, daemon=True).start()

                self.after(0, lambda: self._log("Installer launched successfully.\n"))
                self.after(0, lambda: button_ref.configure(
                    state="normal", text=success_message
                ))
                self.after(0, lambda: messagebox.showinfo("Success", "Installer launched."))

            except Exception as e:
                self.after(0, lambda: self._log(f"Download/launch error: {e}\n"))
                self.after(0, lambda: button_ref.configure(
                    state="normal", text=success_message
                ))
                self.after(0, lambda: messagebox.showerror(T("error"), f"{T('installer_download_failed')}\n{e}"))

        threading.Thread(target=worker, daemon=True).start()

    def _run_steamtools(self):
        exe = r"C:\Program Files\SteamTools\SteamTools.exe"
        if not os.path.exists(exe):
            messagebox.showerror("Not Found", f"SteamTools not found at:\n{exe}")
            self._log(f"  Run SteamTools: not found at {exe}\n")
            return
        try:
            subprocess.Popen(["explorer.exe", exe])
            self._log("  SteamTools launched (as regular user).\n")
        except Exception as e:
            messagebox.showerror(T("error"), f"Could not launch SteamTools:\n{e}")
            self._log(f"  Run SteamTools error: {e}\n")

    def _rem_update_path_label(self):
        if self._rem_steam_path:
            p = self._rem_steam_path
            display = p[:40] + "..." if len(p) > 44 else p
            self._rem_path_lbl.configure(
                text=f"{T('steam_path_label')} {display}", text_color=Theme.TEXT_MUTED
            )
        else:
            self._rem_path_lbl.configure(
                text=T("steam_path_notfound"), text_color=Theme.WARNING,
            )

    def _rem_change_path(self):
        new_path = filedialog.askdirectory(initialdir=self._rem_steam_path or os.path.expanduser("~"))
        if not new_path:
            return
        if os.path.exists(os.path.join(new_path, "Steam.exe")):
            self._rem_steam_path = new_path
            self._rem_update_path_label()
            self._migrated = False
            self.after(100, self._migrate_old_files)
        else:
            messagebox.showwarning(T("invalid_path"), T("invalid_path_msg", path=new_path))

    def _rem_remove_game(self):
        if not self._rem_steam_path:
            messagebox.showerror(T("no_steam_folder"), T("no_steam_msg"))
            return
        RemoveGameDialog(self, self._rem_steam_path, self._rem_game_done)

    def _rem_game_done(self, app_id: str, game_label: str, files_deleted: int, log_text: str):
        self._log(f"Remove Game — {game_label}: {files_deleted} file(s) deleted.\n")
        if files_deleted > 0:
            messagebox.showinfo(
                T("remove_done_title"),
                T("remove_done_msg", n=files_deleted, label=game_label),
            )
        else:
            messagebox.showinfo(
                T("remove_none_title"),
                T("remove_none_msg", label=game_label),
            )

    def _rem_remove_all_games(self):
        if not self._rem_steam_path:
            messagebox.showerror(T("no_steam_folder"), T("no_steam_msg2"))
            return
        if not messagebox.askyesno(T("remove_all_confirm"), T("remove_all_msg")):
            self._log("Remove All Games — aborted.\n")
            return

        steam_path = self._rem_steam_path
        lua_dir = os.path.join(steam_path, "config", "lua")
        depotcache_dir = os.path.join(steam_path, "config", "depotcache")
        total_deleted = 0

        if os.path.isdir(lua_dir):
            for fname in os.listdir(lua_dir):
                if fname.endswith(".lua"):
                    try:
                        os.remove(os.path.join(lua_dir, fname))
                        total_deleted += 1
                        self._log(f"  Deleted: config/lua/{fname}\n")
                    except OSError:
                        pass

        if os.path.isdir(depotcache_dir):
            for fname in os.listdir(depotcache_dir):
                if fname.endswith(".manifest"):
                    try:
                        os.remove(os.path.join(depotcache_dir, fname))
                        total_deleted += 1
                        self._log(f"  Deleted: config/depotcache/{fname}\n")
                    except OSError:
                        pass

        self._log(f"Remove All Games — {total_deleted} file(s) deleted.\n")
        messagebox.showinfo(T("remove_all_done"), T("remove_all_done_msg", n=total_deleted))

    def _rem_restart_steam(self):
        if not self._rem_steam_path:
            self.after(0, lambda: messagebox.showerror(T("no_steam_folder"), T("no_steam_msg2")))
            return
        steam_exe = os.path.join(self._rem_steam_path, "Steam.exe")
        if not os.path.exists(steam_exe):
            self.after(0, lambda: messagebox.showerror("Not Found", f"Steam.exe not found:\n{steam_exe}"))
            return
        try:
            si = subprocess.STARTUPINFO()
            si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            subprocess.run(["taskkill", "/IM", "Steam.exe", "/F"],
                           startupinfo=si, check=False, capture_output=True)
            time.sleep(1)
            subprocess.Popen([steam_exe])
            self.after(0, lambda: self._log("Steam restarted.\n"))
        except Exception as e:
            self.after(0, lambda err=e: messagebox.showerror(T("error"), T("restart_error", err=err)))


if __name__ == "__main__":
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("blue")
    app = App()
    app.mainloop()