import os
import sys
from typing import List, Tuple, Union

import folium

current_dir = os.path.dirname(os.path.realpath(__file__))
src_dir = os.path.join(current_dir, "..", "..", "..")
sys.path.append(src_dir)
from yuheng import Carto
from yuheng.component import Member, Node, Relation, Way


class VizFolium:
    def __init__(self):
        self.config_node_display_method = "marker"
        self.element_list = []
        self.sample_node = Node({"id": "114"}, {})
        self.sample_way = Way({"id": "514"}, {}, [])
        self.sample_relation = Relation(
            {"id": "1919"},
            {},
            [
                Member(
                    element_type="node",
                    role="vip_restaurant",
                    ref=810,
                )
            ],
        )
        self.sample_carto = Carto()

    def add(self, element: Union[Carto, Way, Node, Relation]) -> None:
        """
        Append some element to list
        """
        self.element_list.append(element)
        return None

    @staticmethod
    def transform(
        self,
        element: Union[Node, Way, Relation],
        element_type="",
        reference_carto=None,
    ) -> Union[Tuple[float, float], List[Tuple[float, float]]]:
        if element_type == "node" or isinstance(
            element, type(self.sample_node)
        ):
            lat = element.lat
            lon = element.lon
            return tuple([lat, lon])
        elif element_type == "way" or isinstance(
            element, type(self.sample_way)
        ):
            nd_list = element.nds
            nd_shape_list = []
            node_space = self.element_list
            if reference_carto != None:
                node_space = [v for k, v in reference_carto.node_dict.items()]
            for node in nd_list:
                for iter_ele in node_space:
                    if (
                        isinstance(iter_ele, type(Node({"id": "114"}, {})))
                        and iter_ele.id == node
                    ):
                        nd_shape_list.append((iter_ele.lat, iter_ele.lon))
            return nd_shape_list

    def display(self, **kwargs) -> None:
        """
        This func display some element to html

        If **kwargs is not blank, then we should call self.add() for each one, then display as expected.
        """
        import webbrowser

        if (len(kwargs)) > 0:
            print(f"There are {len(kwargs)} object need to append")
            for k, v in kwargs.items():
                self.add(v)

        m = folium.Map(location=[0, 0], zoom_start=0)
        # # You can replace with custom tiles
        # m = folium.Map(
        #     tiles="https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png",
        #     attr=" ".join(
        #         [
        #             f'&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
        #             f'&copy; <a href="https://carto.com/attributions">CARTO</a>',
        #         ]
        #     ),
        # )

        for element in self.element_list:
            if isinstance(element, type(self.sample_node)):
                print("This is a Node")

                if self.config_node_display_method == "marker":
                    folium.Marker(list(self.transform(self, element))).add_to(
                        m
                    )
                elif self.config_node_display_method == "short_line":
                    folium.PolyLine(
                        [
                            self.transform(self, element),
                            self.transform(self, element),
                        ]
                    ).add_to(m)
                else:
                    pass

            if isinstance(element, type(self.sample_way)):
                print("This is a Way")
                folium.PolyLine(self.transform(self, element)).add_to(m)
            if isinstance(
                element,
                type(self.sample_relation),
            ):
                print("This is a Relation")
            if isinstance(element, type(self.sample_carto)):
                import time

                print("Wow a hole map!")
                # batch time control
                work_burden = (
                    len(element.node_dict)
                    + len(element.way_dict)
                    + len(element.relation_dict)
                )
                work_burden_report_node_interval = 1000
                work_burden_report_way_interval = 15
                # node
                time_node_start = time.time()
                work_burden_node_count = 0
                for id, obj in element.node_dict.items():
                    # print(f"world-node-{id}") # debug
                    work_burden_node_count += 1
                    folium.ColorLine(
                        positions=[(obj.lat, obj.lon), (obj.lat, obj.lon)],
                        colors=[0.114514, 0.1919810],
                        colormap=["black", "black"],
                        weight=4,
                    ).add_to(m)
                    if (
                        work_burden > work_burden_report_node_interval
                        and work_burden_node_count
                        % work_burden_report_node_interval
                        == 0
                    ):
                        time_node_this = time.time()
                        print(
                            "[time] display "
                            + str(work_burden_node_count)
                            + " node use "
                            + str(time_node_this - time_node_start)
                            + " s"
                        )
                time_node_end = time.time()
                print(
                    "[time] display **all** node use "
                    + str(time_node_end - time_node_start)
                    + " s"
                )
                # way
                time_way_start = time.time()
                work_burden_way_count = 0
                for id, obj in element.way_dict.items():
                    # print(f"world-way-{id}", len(obj.nds)) # debug
                    if len(obj.nds) >= 0:
                        work_burden_way_count += 1
                        folium.PolyLine(
                            self.transform(self, obj, reference_carto=element),
                            weight=2,
                        ).add_to(m)
                        if (
                            work_burden > work_burden_report_way_interval
                            and work_burden_way_count
                            % work_burden_report_way_interval
                            == 0
                        ):
                            time_way_this = time.time()
                            print(
                                "[time] display "
                                + str(work_burden_way_count)
                                + " way use "
                                + str(time_way_this - time_way_start)
                                + " s"
                            )
                time_way_end = time.time()
                print(
                    "[time] display **all** way use "
                    + str(time_way_end - time_way_start)
                    + " s"
                )

        # gen html file or call webbrowser
        time_save_html_start = time.time()
        m.save("index.html")
        time_save_html_end = time.time()
        print(
            "[time] save html use "
            + str(time_save_html_end - time_save_html_start)
            + " s"
        )
        # webbrowser.open(
        #     url=os.path.join(
        #         os.path.dirname(os.path.realpath(__file__)), "index.html"
        #     ),
        #     new=1,
        # )
        return None


def main() -> None:
    print("This plugin can't be run as module.")


if __name__ == "__main__":
    main()
