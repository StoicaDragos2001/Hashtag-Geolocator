import io
import folium
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView
from alive_progress import alive_bar


class Geolocator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Twitter Hashtag Geolocator")
        self.setMinimumSize(1200, 800)

        self.qt_layout = QVBoxLayout()
        self.setLayout(self.qt_layout)

        self.world_map = folium.Map(
            location=[0, 0],
            zoom_start=2,
        )

    def add_data(self, entries):
        geolocation_dictionary = {}
        print(f"DateTime of last {len(entries)} entries:")
        for index in range(len(entries)):
            print(entries[index][str(index)]["date"])
            lat, long = entries[index][str(index)]["latitude"], entries[index][str(index)]["longitude"]
            if (lat, long) in geolocation_dictionary:
                geolocation_dictionary[(lat, long)].extend(
                    [str(entries[index][str(index)]["id"]), entries[index][str(index)]["screen_name"]])
            else:
                geolocation_dictionary[(lat, long)] = [str(entries[index][str(index)]["id"]),
                                                       entries[index][str(index)]["screen_name"]]
        print("Data to plot:")
        with alive_bar(spinner="classic", force_tty=True, title="Generating Map", dual_line=True) as bar:
            for (lat, long), values in geolocation_dictionary.items():
                print((lat, long), ":", values)
                if len(values) > 2:
                    folium.Marker(
                        location=[lat, long],
                        popup="\n".join("https://twitter.com/twitter/statuses/" + tweet_id for tweet_id in values[::2]),
                        tooltip=", ".join(screen_name for screen_name in values[1::2])
                    ).add_to(self.world_map)
                else:
                    folium.Marker(
                        location=[lat, long],
                        popup="https://twitter.com/twitter/statuses/" + values[0],
                        tooltip=values[1]
                    ).add_to(self.world_map)
                bar()

        map_data = io.BytesIO()
        self.world_map.save(map_data, close_file=False)

        web_view = QWebEngineView()
        web_view.setHtml(map_data.getvalue().decode())
        self.qt_layout.addWidget(web_view)
