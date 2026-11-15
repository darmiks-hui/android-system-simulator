from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.utils import platform

TRANSLATIONS = {
    "ru": {
        "title": "УСТРОЙСТВО",
        "lang_btn": "EN",
        "refresh": "Обн.",
        "exit": "ВЫЙТИ",

        "section_device": "Устройство",
        "section_battery": "Батарея",
        "section_memory": "Память",
        "section_storage": "Хранилище",
        "section_display": "Экран",
        "section_network": "Сеть",
        "section_cpu": "Процессор",
        "section_sensors": "Датчики",
        "section_modules": "Модули связи",
        "section_system": "Система",
        "section_summary": "Итог диагностики",

        "manufacturer": "Производитель",
        "model": "Модель",
        "android_version": "Версия Android",
        "sdk": "SDK",
        "board": "Платформа",
        "fingerprint": "Сборка (fingerprint)",

        "battery_level": "Заряд",
        "battery_status": "Статус",
        "battery_temp": "Температура",
        "battery_health": "Состояние",

        "ram_total": "Всего RAM",
        "ram_free": "Свободно RAM",

        "storage_total": "Всего места",
        "storage_free": "Свободно места",

        "resolution": "Разрешение",
        "density": "Плотность",
        "refresh_rate": "Частота обновления",
        "orientation": "Ориентация",

        "network_type": "Тип подключения",
        "network_connected": "Подключено",
        "operator": "Оператор",

        "cpu_abi": "Архитектура",
        "cpu_cores": "Количество ядер",

        "sensors_list": "Доступные датчики",

        "bluetooth": "Bluetooth",
        "nfc": "NFC",
        "gps": "GPS",

        "uptime": "Время работы",
        "locale": "Язык системы",
        "timezone": "Часовой пояс",

        "yes": "Да",
        "no": "Нет",
        "na": "Недоступно",
        "charging": "Заряжается",
        "discharging": "Разряжается",
        "full": "Заряжена",
        "unknown": "Неизвестно",
        "good": "Хорошее",
        "portrait": "Портретная",
        "landscape": "Альбомная",

        "verdict_battery_temp": "Температура батареи",
        "verdict_battery_health": "Состояние батареи",
        "verdict_storage": "Свободное место",
        "verdict_network": "Подключение к сети",

        "verdict_good": "Хорошо",
        "verdict_warn": "Повышено",
        "verdict_bad": "Критично",
        "verdict_na": "Нет данных",
        "verdict_storage_low": "Мало места",
        "verdict_storage_critical": "Критически мало места",
        "verdict_network_connected": "Подключено",
        "verdict_network_disconnected": "Нет подключения",
    },
    "en": {
        "title": "DEVICE INFO",
        "lang_btn": "RU",
        "refresh": "Refr.",
        "exit": "EXIT",

        "section_device": "Device",
        "section_battery": "Battery",
        "section_memory": "Memory",
        "section_storage": "Storage",
        "section_display": "Display",
        "section_network": "Network",
        "section_cpu": "Processor",
        "section_sensors": "Sensors",
        "section_modules": "Connectivity Modules",
        "section_system": "System",
        "section_summary": "Diagnostic Summary",

        "manufacturer": "Manufacturer",
        "model": "Model",
        "android_version": "Android Version",
        "sdk": "SDK",
        "board": "Board",
        "fingerprint": "Build Fingerprint",

        "battery_level": "Level",
        "battery_status": "Status",
        "battery_temp": "Temperature",
        "battery_health": "Health",

        "ram_total": "Total RAM",
        "ram_free": "Free RAM",

        "storage_total": "Total Storage",
        "storage_free": "Free Storage",

        "resolution": "Resolution",
        "density": "Density",
        "refresh_rate": "Refresh Rate",
        "orientation": "Orientation",

        "network_type": "Connection Type",
        "network_connected": "Connected",
        "operator": "Carrier",

        "cpu_abi": "Architecture",
        "cpu_cores": "CPU Cores",

        "sensors_list": "Available Sensors",

        "bluetooth": "Bluetooth",
        "nfc": "NFC",
        "gps": "GPS",

        "uptime": "Uptime",
        "locale": "System Language",
        "timezone": "Timezone",

        "yes": "Yes",
        "no": "No",
        "na": "N/A",
        "charging": "Charging",
        "discharging": "Discharging",
        "full": "Full",
        "unknown": "Unknown",
        "good": "Good",
        "portrait": "Portrait",
        "landscape": "Landscape",

        "verdict_battery_temp": "Battery Temperature",
        "verdict_battery_health": "Battery Health",
        "verdict_storage": "Free Storage",
        "verdict_network": "Network Connection",

        "verdict_good": "Good",
        "verdict_warn": "Elevated",
        "verdict_bad": "Critical",
        "verdict_na": "No Data",
        "verdict_storage_low": "Low Space",
        "verdict_storage_critical": "Critically Low Space",
        "verdict_network_connected": "Connected",
        "verdict_network_disconnected": "Not Connected",
    },
}


def get_android_info():
    """Собирает реальные данные об устройстве через pyjnius.
    Если что-то недоступно (например при тесте вне Android),
    подставляется None и при отрисовке показывается как N/A."""

    data = {
        "manufacturer": None, "model": None, "android_version": None,
        "sdk": None, "board": None, "fingerprint": None,

        "battery_level": None, "battery_status": None,
        "battery_temp": None, "battery_health": None,

        "ram_total": None, "ram_free": None,

        "storage_total": None, "storage_free": None,

        "refresh_rate": None,

        "network_type": None, "network_connected": None, "operator": None,

        "cpu_abi": None, "cpu_cores": None,

        "sensors_list": None,

        "bluetooth": None, "nfc": None, "gps": None,

        "uptime": None, "locale": None, "timezone": None,
    }

    if platform != "android":
        return data

    # --- Устройство / сборка ---
    try:
        from jnius import autoclass

        Build = autoclass("android.os.Build")
        VERSION = autoclass("android.os.Build$VERSION")

        data["manufacturer"] = Build.MANUFACTURER
        data["model"] = Build.MODEL
        data["android_version"] = VERSION.RELEASE
        data["sdk"] = VERSION.SDK_INT
        data["board"] = Build.BOARD
        data["fingerprint"] = Build.FINGERPRINT

        try:
            abis = Build.SUPPORTED_ABIS
            data["cpu_abi"] = abis[0] if abis else None
        except Exception:
            data["cpu_abi"] = Build.CPU_ABI if hasattr(Build, "CPU_ABI") else None
    except Exception:
        pass

    # --- Батарея ---
    try:
        from jnius import autoclass

        PythonActivity = autoclass("org.kivy.android.PythonActivity")
        Intent = autoclass("android.content.Intent")
        IntentFilter = autoclass("android.content.IntentFilter")
        BatteryManager = autoclass("android.os.BatteryManager")

        activity = PythonActivity.mActivity
        intent_filter = IntentFilter(Intent.ACTION_BATTERY_CHANGED)
        battery_status = activity.registerReceiver(None, intent_filter)

        level = battery_status.getIntExtra(BatteryManager.EXTRA_LEVEL, -1)
        scale = battery_status.getIntExtra(BatteryManager.EXTRA_SCALE, -1)
        if scale > 0:
            data["battery_level"] = int(level / scale * 100)

        status = battery_status.getIntExtra(BatteryManager.EXTRA_STATUS, -1)
        status_map = {2: "charging", 3: "discharging", 5: "full"}
        data["battery_status"] = status_map.get(status, "unknown")

        temp = battery_status.getIntExtra(BatteryManager.EXTRA_TEMPERATURE, -1)
        if temp >= 0:
            data["battery_temp"] = round(temp / 10.0, 1)

        health = battery_status.getIntExtra(BatteryManager.EXTRA_HEALTH, -1)
        data["battery_health"] = "good" if health == 2 else "unknown"
    except Exception:
        pass

    # --- Память ---
    try:
        from jnius import autoclass

        PythonActivity = autoclass("org.kivy.android.PythonActivity")
        Context = autoclass("android.content.Context")
        ActivityManager = autoclass("android.app.ActivityManager")
        MemoryInfo = autoclass("android.app.ActivityManager$MemoryInfo")

        activity = PythonActivity.mActivity
        am = activity.getSystemService(Context.ACTIVITY_SERVICE)
        mem_info = MemoryInfo()
        am.getMemoryInfo(mem_info)

        data["ram_total"] = mem_info.totalMem / (1024 ** 3)
        data["ram_free"] = mem_info.availMem / (1024 ** 3)
    except Exception:
        pass

    # --- Хранилище ---
    try:
        from jnius import autoclass

        StatFs = autoclass("android.os.StatFs")
        Environment = autoclass("android.os.Environment")

        path = Environment.getExternalStorageDirectory().getAbsolutePath()
        stat = StatFs(path)
        data["storage_total"] = stat.getTotalBytes() / (1024 ** 3)
        data["storage_free"] = stat.getFreeBytes() / (1024 ** 3)
    except Exception:
        pass

    # --- Сеть ---
    try:
        from jnius import autoclass

        PythonActivity = autoclass("org.kivy.android.PythonActivity")
        Context = autoclass("android.content.Context")
        ConnectivityManager = autoclass("android.net.ConnectivityManager")

        activity = PythonActivity.mActivity
        cm = activity.getSystemService(Context.CONNECTIVITY_SERVICE)
        active_network = cm.getActiveNetworkInfo()
        if active_network is not None:
            data["network_type"] = active_network.getTypeName()
            data["network_connected"] = active_network.isConnected()
        else:
            data["network_connected"] = False
    except Exception:
        pass

    try:
        from jnius import autoclass

        PythonActivity = autoclass("org.kivy.android.PythonActivity")
        Context = autoclass("android.content.Context")
        TelephonyManager = autoclass("android.telephony.TelephonyManager")

        activity = PythonActivity.mActivity
        tm = activity.getSystemService(Context.TELEPHONY_SERVICE)
        operator_name = tm.getNetworkOperatorName()
        data["operator"] = operator_name if operator_name else None
    except Exception:
        pass

    # --- Процессор ---
    try:
        import os
        data["cpu_cores"] = os.cpu_count()
    except Exception:
        pass

    # --- Экран: частота обновления ---
    try:
        from jnius import autoclass

        PythonActivity = autoclass("org.kivy.android.PythonActivity")
        activity = PythonActivity.mActivity
        window_manager = activity.getWindowManager()
        display = window_manager.getDefaultDisplay()
        data["refresh_rate"] = round(display.getRefreshRate(), 1)
    except Exception:
        pass

    # --- Датчики ---
    try:
        from jnius import autoclass

        PythonActivity = autoclass("org.kivy.android.PythonActivity")
        Context = autoclass("android.content.Context")
        SensorManager = autoclass("android.hardware.SensorManager")

        activity = PythonActivity.mActivity
        sm = activity.getSystemService(Context.SENSOR_SERVICE)
        sensor_list = sm.getSensorList(-1)  # TYPE_ALL
        data["sensors_list"] = sensor_list.size()
    except Exception:
        pass

    # --- Bluetooth / NFC / GPS ---
    try:
        from jnius import autoclass

        PythonActivity = autoclass("org.kivy.android.PythonActivity")
        Context = autoclass("android.content.Context")
        PackageManager = autoclass("android.content.pm.PackageManager")

        activity = PythonActivity.mActivity
        pm = activity.getPackageManager()

        data["bluetooth"] = pm.hasSystemFeature(PackageManager.FEATURE_BLUETOOTH)
        data["nfc"] = pm.hasSystemFeature(PackageManager.FEATURE_NFC)
        data["gps"] = pm.hasSystemFeature(PackageManager.FEATURE_LOCATION_GPS)
    except Exception:
        pass

    # --- Аптайм ---
    try:
        from jnius import autoclass

        SystemClock = autoclass("android.os.SystemClock")
        millis = SystemClock.elapsedRealtime()
        total_seconds = int(millis / 1000)
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        data["uptime"] = f"{hours}h {minutes}m"
    except Exception:
        pass

    # --- Локаль и часовой пояс ---
    try:
        from jnius import autoclass

        Locale = autoclass("java.util.Locale")
        current = Locale.getDefault()
        data["locale"] = current.toString()

        TimeZone = autoclass("java.util.TimeZone")
        tz = TimeZone.getDefault()
        data["timezone"] = tz.getID()
    except Exception:
        pass

    return data


def build_verdicts(data):
    """Честные пороговые оценки по реальным измеренным значениям.
    Возвращает список (ключ_метки, статус, ключ_детали_или_None).
    Статус: 'good' | 'warn' | 'bad' | 'na'.
    Намеренно не оценивается свободная RAM — низкий процент свободной
    RAM у Android является нормой (кэширование приложений), а не
    признаком неисправности, и вывод "плохо" был бы недостоверным."""

    verdicts = []

    # Температура батареи (значения в градусах Цельсия)
    temp = data.get("battery_temp")
    if temp is None:
        verdicts.append(("verdict_battery_temp", "na", None))
    elif temp >= 45:
        verdicts.append(("verdict_battery_temp", "bad", None))
    elif temp >= 38:
        verdicts.append(("verdict_battery_temp", "warn", None))
    else:
        verdicts.append(("verdict_battery_temp", "good", None))

    # Состояние батареи (по android.os.BatteryManager.EXTRA_HEALTH)
    health = data.get("battery_health")
    if health is None:
        verdicts.append(("verdict_battery_health", "na", None))
    elif health == "good":
        verdicts.append(("verdict_battery_health", "good", None))
    else:
        verdicts.append(("verdict_battery_health", "warn", None))

    # Свободное место на хранилище
    total = data.get("storage_total")
    free = data.get("storage_free")
    if total is None or free is None or total == 0:
        verdicts.append(("verdict_storage", "na", None))
    else:
        ratio = free / total
        if ratio < 0.10:
            verdicts.append(("verdict_storage", "bad", "verdict_storage_critical"))
        elif ratio < 0.25:
            verdicts.append(("verdict_storage", "warn", "verdict_storage_low"))
        else:
            verdicts.append(("verdict_storage", "good", None))

    # Сеть — информационная строка, не оценка исправности
    connected = data.get("network_connected")
    if connected is None:
        verdicts.append(("verdict_network", "na", None))
    elif connected:
        verdicts.append(("verdict_network", "good", "verdict_network_connected"))
    else:
        verdicts.append(("verdict_network", "warn", "verdict_network_disconnected"))

    return verdicts


class DeviceInfoApp(App):

    def build(self):
        self.lang = "ru"
        Window.clearcolor = (0.015, 0.015, 0.02, 1)

        self.root_layout = BoxLayout(orientation="vertical", padding=15, spacing=10)

        top_bar = BoxLayout(size_hint_y=None, height=64, spacing=18, padding=(4, 6))
        self.title_label = Label(
            text="", markup=True, font_size="20sp",
            color=(0.2, 0.8, 1, 1), halign="left", valign="middle"
        )
        self.title_label.bind(size=self._update_text_size)

        self.refresh_button = Button(size_hint_x=None, width=90, font_size="14sp")
        self.refresh_button.bind(on_press=lambda *_: self.refresh_data())

        self.lang_button = Button(size_hint_x=None, width=70, font_size="14sp")
        self.lang_button.bind(on_press=self.toggle_language)

        top_bar.add_widget(self.title_label)
        top_bar.add_widget(self.refresh_button)
        top_bar.add_widget(self.lang_button)

        self.scroll = ScrollView()
        self.grid = GridLayout(cols=1, size_hint_y=None, spacing=12, padding=(0, 10))
        self.grid.bind(minimum_height=self.grid.setter("height"))
        self.scroll.add_widget(self.grid)

        self.exit_button = Button(
            size_hint=(1, None), height=45,
            background_color=(0.25, 0.25, 0.3, 1)
        )
        self.exit_button.bind(on_press=self.close_app)

        self.root_layout.add_widget(top_bar)
        self.root_layout.add_widget(self.scroll)
        self.root_layout.add_widget(self.exit_button)

        self.refresh_data()
        Clock.schedule_interval(lambda dt: self.refresh_data(), 20)

        return self.root_layout

    def _update_text_size(self, instance, value):
        instance.text_size = (instance.width, instance.height)

    def t(self, key):
        return TRANSLATIONS[self.lang][key]

    def toggle_language(self, instance):
        self.lang = "en" if self.lang == "ru" else "ru"
        self.refresh_data()

    def _section_header(self, text):
        lbl = Label(
            text=f"[b]{text}[/b]", markup=True, font_size="18sp",
            color=(1, 0.3, 0.3, 1), size_hint_y=None, height=40,
            halign="left", valign="middle"
        )
        lbl.bind(size=self._update_text_size)
        return lbl

    def _row(self, label_text, value_text):
        row = GridLayout(cols=2, size_hint_y=None, height=34, spacing=8)
        left = Label(
            text=label_text, font_size="15sp", color=(0.75, 0.75, 0.78, 1),
            halign="left", valign="middle"
        )
        left.bind(size=self._update_text_size)
        right = Label(
            text=str(value_text), font_size="15sp", color=(0.95, 0.95, 1, 1),
            halign="right", valign="middle"
        )
        right.bind(size=self._update_text_size)
        row.add_widget(left)
        row.add_widget(right)
        return row

    def _fmt_bool(self, value):
        if value is None:
            return self.t("na")
        return self.t("yes") if value else self.t("no")

    def _fmt(self, value, suffix=""):
        if value is None:
            return self.t("na")
        return f"{value}{suffix}"

    def _verdict_row(self, label_key, status, detail_key):
        colors = {
            "good": (0.2, 0.85, 0.3, 1),
            "warn": (0.95, 0.7, 0.1, 1),
            "bad": (0.95, 0.2, 0.2, 1),
            "na": (0.6, 0.6, 0.6, 1),
        }
        status_text = detail_key and self.t(detail_key) or self.t(f"verdict_{status}")

        row = GridLayout(cols=2, size_hint_y=None, height=34, spacing=8)
        left = Label(
            text=self.t(label_key), font_size="15sp", color=(0.85, 0.85, 0.9, 1),
            halign="left", valign="middle"
        )
        left.bind(size=self._update_text_size)
        right = Label(
            text=status_text, font_size="15sp", bold=True,
            color=colors.get(status, (0.9, 0.9, 0.9, 1)),
            halign="right", valign="middle"
        )
        right.bind(size=self._update_text_size)
        row.add_widget(left)
        row.add_widget(right)
        return row

    def refresh_data(self):
        data = get_android_info()

        self.title_label.text = f"[b]{self.t('title')}[/b]"
        self.lang_button.text = self.t("lang_btn")
        self.refresh_button.text = self.t("refresh")
        self.exit_button.text = self.t("exit")

        self.grid.clear_widgets()

        # Итог диагностики — в самом верху, чтобы было видно сразу
        self.grid.add_widget(self._section_header(self.t("section_summary")))
        for label_key, status, detail_key in build_verdicts(data):
            self.grid.add_widget(self._verdict_row(label_key, status, detail_key))

        # Устройство
        self.grid.add_widget(self._row(self.t("manufacturer"), self._fmt(data["manufacturer"])))
        self.grid.add_widget(self._row(self.t("model"), self._fmt(data["model"])))
        self.grid.add_widget(self._row(self.t("android_version"), self._fmt(data["android_version"])))
        self.grid.add_widget(self._row(self.t("sdk"), self._fmt(data["sdk"])))
        self.grid.add_widget(self._row(self.t("board"), self._fmt(data["board"])))
        fp = data["fingerprint"]
        fp_short = (fp[:22] + "...") if fp and len(fp) > 22 else self._fmt(fp)
        self.grid.add_widget(self._row(self.t("fingerprint"), fp_short))

        # Процессор
        self.grid.add_widget(self._section_header(self.t("section_cpu")))
        self.grid.add_widget(self._row(self.t("cpu_abi"), self._fmt(data["cpu_abi"])))
        self.grid.add_widget(self._row(self.t("cpu_cores"), self._fmt(data["cpu_cores"])))

        # Батарея
        self.grid.add_widget(self._section_header(self.t("section_battery")))
        self.grid.add_widget(self._row(self.t("battery_level"), self._fmt(data["battery_level"], "%")))
        status_key = data["battery_status"]
        status_text = self.t(status_key) if status_key else self.t("na")
        self.grid.add_widget(self._row(self.t("battery_status"), status_text))
        self.grid.add_widget(self._row(self.t("battery_temp"), self._fmt(data["battery_temp"], " °C")))
        health_key = data["battery_health"]
        health_text = self.t(health_key) if health_key else self.t("na")
        self.grid.add_widget(self._row(self.t("battery_health"), health_text))

        # Память
        self.grid.add_widget(self._section_header(self.t("section_memory")))
        ram_total = data["ram_total"]
        ram_free = data["ram_free"]
        self.grid.add_widget(self._row(
            self.t("ram_total"),
            f"{ram_total:.2f} GB" if ram_total is not None else self.t("na")
        ))
        self.grid.add_widget(self._row(
            self.t("ram_free"),
            f"{ram_free:.2f} GB" if ram_free is not None else self.t("na")
        ))

        # Хранилище
        self.grid.add_widget(self._section_header(self.t("section_storage")))
        st_total = data["storage_total"]
        st_free = data["storage_free"]
        self.grid.add_widget(self._row(
            self.t("storage_total"),
            f"{st_total:.2f} GB" if st_total is not None else self.t("na")
        ))
        self.grid.add_widget(self._row(
            self.t("storage_free"),
            f"{st_free:.2f} GB" if st_free is not None else self.t("na")
        ))

        # Экран
        self.grid.add_widget(self._section_header(self.t("section_display")))
        self.grid.add_widget(self._row(self.t("resolution"), f"{Window.width} x {Window.height}"))
        self.grid.add_widget(self._row(self.t("density"), f"{Window.dpi:.0f} dpi"))
        self.grid.add_widget(self._row(self.t("refresh_rate"), self._fmt(data["refresh_rate"], " Hz")))
        orient_key = "landscape" if Window.width > Window.height else "portrait"
        self.grid.add_widget(self._row(self.t("orientation"), self.t(orient_key)))

        # Сеть
        self.grid.add_widget(self._section_header(self.t("section_network")))
        self.grid.add_widget(self._row(self.t("network_type"), self._fmt(data["network_type"])))
        self.grid.add_widget(self._row(self.t("network_connected"), self._fmt_bool(data["network_connected"])))
        self.grid.add_widget(self._row(self.t("operator"), self._fmt(data["operator"])))

        # Модули связи
        self.grid.add_widget(self._section_header(self.t("section_modules")))
        self.grid.add_widget(self._row(self.t("bluetooth"), self._fmt_bool(data["bluetooth"])))
        self.grid.add_widget(self._row(self.t("nfc"), self._fmt_bool(data["nfc"])))
        self.grid.add_widget(self._row(self.t("gps"), self._fmt_bool(data["gps"])))

        # Датчики
        self.grid.add_widget(self._section_header(self.t("section_sensors")))
        self.grid.add_widget(self._row(self.t("sensors_list"), self._fmt(data["sensors_list"])))

        # Система
        self.grid.add_widget(self._section_header(self.t("section_system")))
        self.grid.add_widget(self._row(self.t("uptime"), self._fmt(data["uptime"])))
        self.grid.add_widget(self._row(self.t("locale"), self._fmt(data["locale"])))
        self.grid.add_widget(self._row(self.t("timezone"), self._fmt(data["timezone"])))

    def close_app(self, instance):
        App.get_running_app().stop()


if __name__ == "__main__":
    DeviceInfoApp().run()
