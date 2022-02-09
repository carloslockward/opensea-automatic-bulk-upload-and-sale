from pathlib import Path
import json


class NewStructure:
    def __init__(self, file_name: str, action=[]) -> None:
        self.file_name = file_name
        self.structure_path = Path(self.file_name)
        self.extension = file_name.split(".")[1]
        self.action = action
        self.data = {}
        self.data_new = {}
        self.curr_id = 0

        if not self.structure_path.exists():
            raise Exception(f'File "{self.file_name}" doesnt exists!')

        self.read_file()

    def read_file(self):
        if self.extension not in ["json"]:
            raise Exception(f'Unsupported file extension ".{self.extension}"')
        elif self.extension == "json":
            with self.structure_path.open("r") as f:
                data = json.load(f)
            # Check if the file is in the old format.
            if "nft" in data.keys():
                if isinstance(data["nft"], list):
                    if len(data["nft"]) > 0:
                        self.data = data["nft"]
                        for nft_data in data["nft"]:
                            new_data = nft_data.copy()
                            name = new_data.pop("nft_name")
                            self.data_new[name] = new_data
                else:
                    raise Exception("Invalid file format")
            else:
                self.data_new = data
                nft_list = []
                for nft_name in list(data.keys()):
                    elem = data[nft_name].copy()
                    elem["nft_name"] = nft_name
                    nft_list.append(elem)
                self.data = nft_list

    def __len__(self):
        return len(self.data)

    def get_data(self, nft_identifier):
        self.curr_id = nft_identifier
        if isinstance(nft_identifier, str):
            nft_data = self.data_new[nft_identifier]
            nft_name = nft_identifier
        elif isinstance(nft_identifier, int):
            nft_data = self.data[nft_identifier]
            nft_name = nft_data["nft_name"]
        else:
            raise Exception(
                f'NFT identifier of unsupported type! "{type(nft_identifier)}"'
            )

        if len(self.action) > 0:
            if 1 in self.action:  # Upload part.
                self.file_path: str or list = nft_data["file_path"]
                self.nft_name: str = str(nft_name)  # Set string value to
                self.link: str = str(
                    nft_data["external_link"]
                )  # real string to prevent
                self.description: str = str(nft_data["description"])  # different types.
                self.collection: str = str(nft_data["collection"])
                self.properties: list = nft_data["properties"]  # [[type, name], ...].
                self.levels: list = nft_data["levels"]  # [[name, from, to], ...].
                self.stats: list = nft_data["stats"]  # [[name, from, to], ...].
                self.unlockable_content: list or bool = nft_data[
                    "unlockable_content"
                ]  # [bool, str].
                self.explicit_sensitive: bool = nft_data[
                    "explicit_and_sensitive_content"
                ]
                self.supply: int = nft_data["supply"]
                self.blockchain: str = str(nft_data["blockchain"]).capitalize()
            if 2 in self.action:  # Sale part.
                self.type: str = str(nft_data["sale_type"]).title()
                self.price: float or int = nft_data["price"]
                self.method: list = nft_data["method"]  # [method, price].
                self.duration: list or str = nft_data["duration"]
                self.specific_buyer: list or bool = nft_data["specific_buyer"]
                self.quantity: int = nft_data["quantity"]
            if len(self.action) == 1 and self.action[0] == 2:  # Sale only!
                self.nft_url: str = str(nft_data["nft_url"])
                self.supply: int = nft_data["supply"]
                self.blockchain: str = str(nft_data["blockchain"]).capitalize()
            if "slug" in nft_data.keys():
                self.slug = nft_data["slug"]

    def __getitem__(self, item: int or str):
        """getitem to make object subscriptable

        Args:
            item (int or str): [description]

        Returns:
            [type]: [description]
        """

        self.get_data(item)

        return self

    def save(self):
        with self.structure_path.open("w") as f:
            json.dump(self.data_new, f, indent=4)

    # def __del__(self):
    #    with self.structure_path.open("w") as f:
    #        json.dump(self.data_new, f, indent=4)

    def save_nft(self, url):
        self.nft_url = url
        self.save()

    @property
    def number(self):
        if isinstance(self.curr_id, str):
            return list(self.data_new.keys()).index(self.curr_id)
        elif isinstance(self.curr_id, int):
            return self.curr_id

    @property
    def file_path(self):
        if isinstance(self.curr_id, str):
            return self.data_new[self.curr_id]["file_path"]
        elif isinstance(self.curr_id, int):
            return self.data[self.curr_id]["file_path"]
        else:
            raise Exception(
                f'NFT identifier of unsupported type! "{type(self.curr_id)}"'
            )

    @file_path.setter
    def file_path(self, value):
        if isinstance(self.curr_id, str):
            self.data_new[self.curr_id]["file_path"] = value
        elif isinstance(self.curr_id, int):
            self.data[self.curr_id]["file_path"] = value
        else:
            raise Exception(
                f'NFT identifier of unsupported type! "{type(self.curr_id)}"'
            )

    @property
    def nft_name(self):
        if isinstance(self.curr_id, str):
            return self.data_new[self.curr_id]["nft_name"]
        elif isinstance(self.curr_id, int):
            return self.data[self.curr_id]["nft_name"]
        else:
            raise Exception(
                f'NFT identifier of unsupported type! "{type(self.curr_id)}"'
            )

    @nft_name.setter
    def nft_name(self, value):
        if isinstance(self.curr_id, str):
            self.data_new[self.curr_id]["nft_name"] = str(value)
        elif isinstance(self.curr_id, int):
            self.data[self.curr_id]["nft_name"] = str(value)
        else:
            raise Exception(
                f'NFT identifier of unsupported type! "{type(self.curr_id)}"'
            )

    @property
    def link(self):
        if isinstance(self.curr_id, str):
            return self.data_new[self.curr_id]["external_link"]
        elif isinstance(self.curr_id, int):
            return self.data[self.curr_id]["external_link"]
        else:
            raise Exception(
                f'NFT identifier of unsupported type! "{type(self.curr_id)}"'
            )

    @link.setter
    def link(self, value):
        if isinstance(self.curr_id, str):
            self.data_new[self.curr_id]["external_link"] = str(value)
        elif isinstance(self.curr_id, int):
            self.data[self.curr_id]["external_link"] = str(value)
        else:
            raise Exception(
                f'NFT identifier of unsupported type! "{type(self.curr_id)}"'
            )

    @property
    def description(self):
        if isinstance(self.curr_id, str):
            return self.data_new[self.curr_id]["description"]
        elif isinstance(self.curr_id, int):
            return self.data[self.curr_id]["description"]
        else:
            raise Exception(
                f'NFT identifier of unsupported type! "{type(self.curr_id)}"'
            )

    @description.setter
    def description(self, value):
        if isinstance(self.curr_id, str):
            self.data_new[self.curr_id]["description"] = str(value)
        elif isinstance(self.curr_id, int):
            self.data[self.curr_id]["description"] = str(value)
        else:
            raise Exception(
                f'NFT identifier of unsupported type! "{type(self.curr_id)}"'
            )

    @property
    def collection(self):
        if isinstance(self.curr_id, str):
            return self.data_new[self.curr_id]["collection"]
        elif isinstance(self.curr_id, int):
            return self.data[self.curr_id]["collection"]
        else:
            raise Exception(
                f'NFT identifier of unsupported type! "{type(self.curr_id)}"'
            )

    @collection.setter
    def collection(self, value):
        if isinstance(self.curr_id, str):
            self.data_new[self.curr_id]["collection"] = str(value)
        elif isinstance(self.curr_id, int):
            self.data[self.curr_id]["collection"] = str(value)
        else:
            raise Exception(
                f'NFT identifier of unsupported type! "{type(self.curr_id)}"'
            )

    @property
    def properties(self):
        if isinstance(self.curr_id, str):
            props = self.data_new[self.curr_id]["properties"]
        elif isinstance(self.curr_id, int):
            props = self.data[self.curr_id]["properties"]
        else:
            raise Exception(
                f'NFT identifier of unsupported type! "{type(self.curr_id)}"'
            )
        final_list = []
        if isinstance(props, list) and len(props) > 0:
            for elem in props:
                elem_list = []
                for key in list(elem.keys()):
                    elem_list.append(elem[key])
                final_list.append(elem_list)
        return final_list

    @properties.setter
    def properties(self, value):
        if isinstance(self.curr_id, str):
            self.data_new[self.curr_id]["properties"] = value
        elif isinstance(self.curr_id, int):
            self.data[self.curr_id]["properties"] = value
        else:
            raise Exception(
                f'NFT identifier of unsupported type! "{type(self.curr_id)}"'
            )

    @property
    def levels(self):
        if isinstance(self.curr_id, str):
            levs = self.data_new[self.curr_id]["levels"]
        elif isinstance(self.curr_id, int):
            levs = self.data[self.curr_id]["levels"]
        else:
            raise Exception(
                f'NFT identifier of unsupported type! "{type(self.curr_id)}"'
            )
        final_list = []
        if isinstance(levs, list) and len(levs) > 0:
            for elem in levs:
                elem_list = []
                for key in list(elem.keys()):
                    elem_list.append(elem[key])
                final_list.append(elem_list)
        return final_list

    @levels.setter
    def levels(self, value):
        if isinstance(self.curr_id, str):
            self.data_new[self.curr_id]["levels"] = value
        elif isinstance(self.curr_id, int):
            self.data[self.curr_id]["levels"] = value
        else:
            raise Exception(
                f'NFT identifier of unsupported type! "{type(self.curr_id)}"'
            )

    @property
    def stats(self):
        if isinstance(self.curr_id, str):
            stats = self.data_new[self.curr_id]["stats"]
        elif isinstance(self.curr_id, int):
            stats = self.data[self.curr_id]["stats"]
        else:
            raise Exception(
                f'NFT identifier of unsupported type! "{type(self.curr_id)}"'
            )
        final_list = []
        if isinstance(stats, list) and len(stats) > 0:
            for elem in stats:
                elem_list = []
                for key in list(elem.keys()):
                    elem_list.append(elem[key])
                final_list.append(elem_list)
        return final_list

    @stats.setter
    def stats(self, value):
        if isinstance(self.curr_id, str):
            self.data_new[self.curr_id]["stats"] = value
        elif isinstance(self.curr_id, int):
            self.data[self.curr_id]["stats"] = value
        else:
            raise Exception(
                f'NFT identifier of unsupported type! "{type(self.curr_id)}"'
            )

    @property
    def unlockable_content(self):
        if isinstance(self.curr_id, str):
            return self.data_new[self.curr_id]["unlockable_content"]
        elif isinstance(self.curr_id, int):
            return self.data[self.curr_id]["unlockable_content"]
        else:
            raise Exception(
                f'NFT identifier of unsupported type! "{type(self.curr_id)}"'
            )

    @unlockable_content.setter
    def unlockable_content(self, value):
        if isinstance(self.curr_id, str):
            self.data_new[self.curr_id]["unlockable_content"] = value
        elif isinstance(self.curr_id, int):
            self.data[self.curr_id]["unlockable_content"] = value
        else:
            raise Exception(
                f'NFT identifier of unsupported type! "{type(self.curr_id)}"'
            )

    @property
    def explicit_sensitive(self):
        if isinstance(self.curr_id, str):
            return self.data_new[self.curr_id]["explicit_and_sensitive_content"]
        elif isinstance(self.curr_id, int):
            return self.data[self.curr_id]["explicit_and_sensitive_content"]
        else:
            raise Exception(
                f'NFT identifier of unsupported type! "{type(self.curr_id)}"'
            )

    @explicit_sensitive.setter
    def explicit_sensitive(self, value):
        if isinstance(self.curr_id, str):
            self.data_new[self.curr_id]["explicit_and_sensitive_content"] = value
        elif isinstance(self.curr_id, int):
            self.data[self.curr_id]["explicit_and_sensitive_content"] = value
        else:
            raise Exception(
                f'NFT identifier of unsupported type! "{type(self.curr_id)}"'
            )

    @property
    def supply(self):
        if isinstance(self.curr_id, str):
            return self.data_new[self.curr_id]["supply"]
        elif isinstance(self.curr_id, int):
            return self.data[self.curr_id]["supply"]
        else:
            raise Exception(
                f'NFT identifier of unsupported type! "{type(self.curr_id)}"'
            )

    @supply.setter
    def supply(self, value):
        if isinstance(self.curr_id, str):
            self.data_new[self.curr_id]["supply"] = value
        elif isinstance(self.curr_id, int):
            self.data[self.curr_id]["supply"] = value
        else:
            raise Exception(
                f'NFT identifier of unsupported type! "{type(self.curr_id)}"'
            )

    @property
    def blockchain(self):
        if isinstance(self.curr_id, str):
            return self.data_new[self.curr_id]["blockchain"]
        elif isinstance(self.curr_id, int):
            return self.data[self.curr_id]["blockchain"]
        else:
            raise Exception(
                f'NFT identifier of unsupported type! "{type(self.curr_id)}"'
            )

    @blockchain.setter
    def blockchain(self, value):
        if isinstance(self.curr_id, str):
            self.data_new[self.curr_id]["blockchain"] = str(value).capitalize()
        elif isinstance(self.curr_id, int):
            self.data[self.curr_id]["blockchain"] = str(value).capitalize()
        else:
            raise Exception(
                f'NFT identifier of unsupported type! "{type(self.curr_id)}"'
            )

    @property
    def type(self):
        if isinstance(self.curr_id, str):
            return self.data_new[self.curr_id]["sale_type"]
        elif isinstance(self.curr_id, int):
            return self.data[self.curr_id]["sale_type"]
        else:
            raise Exception(
                f'NFT identifier of unsupported type! "{type(self.curr_id)}"'
            )

    @type.setter
    def type(self, value):
        if isinstance(self.curr_id, str):
            self.data_new[self.curr_id]["sale_type"] = str(value).title()
        elif isinstance(self.curr_id, int):
            self.data[self.curr_id]["sale_type"] = str(value).title()
        else:
            raise Exception(
                f'NFT identifier of unsupported type! "{type(self.curr_id)}"'
            )

    @property
    def price(self):
        if isinstance(self.curr_id, str):
            return self.data_new[self.curr_id]["price"]
        elif isinstance(self.curr_id, int):
            return self.data[self.curr_id]["price"]
        else:
            raise Exception(
                f'NFT identifier of unsupported type! "{type(self.curr_id)}"'
            )

    @price.setter
    def price(self, value):
        if isinstance(self.curr_id, str):
            self.data_new[self.curr_id]["price"] = value
        elif isinstance(self.curr_id, int):
            self.data[self.curr_id]["price"] = value
        else:
            raise Exception(
                f'NFT identifier of unsupported type! "{type(self.curr_id)}"'
            )

    @property
    def method(self):
        if isinstance(self.curr_id, str):
            return self.data_new[self.curr_id]["method"]
        elif isinstance(self.curr_id, int):
            return self.data[self.curr_id]["method"]
        else:
            raise Exception(
                f'NFT identifier of unsupported type! "{type(self.curr_id)}"'
            )

    @method.setter
    def method(self, value):
        if isinstance(self.curr_id, str):
            self.data_new[self.curr_id]["method"] = value
        elif isinstance(self.curr_id, int):
            self.data[self.curr_id]["method"] = value
        else:
            raise Exception(
                f'NFT identifier of unsupported type! "{type(self.curr_id)}"'
            )

    @property
    def duration(self):
        if isinstance(self.curr_id, str):
            return self.data_new[self.curr_id]["duration"]
        elif isinstance(self.curr_id, int):
            return self.data[self.curr_id]["duration"]
        else:
            raise Exception(
                f'NFT identifier of unsupported type! "{type(self.curr_id)}"'
            )

    @duration.setter
    def duration(self, value):
        if isinstance(self.curr_id, str):
            self.data_new[self.curr_id]["duration"] = value
        elif isinstance(self.curr_id, int):
            self.data[self.curr_id]["duration"] = value
        else:
            raise Exception(
                f'NFT identifier of unsupported type! "{type(self.curr_id)}"'
            )

    @property
    def specific_buyer(self):
        if isinstance(self.curr_id, str):
            return self.data_new[self.curr_id]["specific_buyer"]
        elif isinstance(self.curr_id, int):
            return self.data[self.curr_id]["specific_buyer"]
        else:
            raise Exception(
                f'NFT identifier of unsupported type! "{type(self.curr_id)}"'
            )

    @specific_buyer.setter
    def specific_buyer(self, value):
        if isinstance(self.curr_id, str):
            self.data_new[self.curr_id]["specific_buyer"] = value
        elif isinstance(self.curr_id, int):
            self.data[self.curr_id]["specific_buyer"] = value
        else:
            raise Exception(
                f'NFT identifier of unsupported type! "{type(self.curr_id)}"'
            )

    @property
    def quantity(self):
        if isinstance(self.curr_id, str):
            return self.data_new[self.curr_id]["quantity"]
        elif isinstance(self.curr_id, int):
            return self.data[self.curr_id]["quantity"]
        else:
            raise Exception(
                f'NFT identifier of unsupported type! "{type(self.curr_id)}"'
            )

    @quantity.setter
    def quantity(self, value):
        if isinstance(self.curr_id, str):
            self.data_new[self.curr_id]["quantity"] = value
        elif isinstance(self.curr_id, int):
            self.data[self.curr_id]["quantity"] = value
        else:
            raise Exception(
                f'NFT identifier of unsupported type! "{type(self.curr_id)}"'
            )

    @property
    def nft_url(self):
        if isinstance(self.curr_id, str):
            return self.data_new[self.curr_id]["nft_url"]
        elif isinstance(self.curr_id, int):
            return self.data[self.curr_id]["nft_url"]
        else:
            raise Exception(
                f'NFT identifier of unsupported type! "{type(self.curr_id)}"'
            )

    @nft_url.setter
    def nft_url(self, value):
        if isinstance(self.curr_id, str):
            self.data_new[self.curr_id]["nft_url"] = str(value)
        elif isinstance(self.curr_id, int):
            self.data[self.curr_id]["nft_url"] = str(value)
        else:
            raise Exception(
                f'NFT identifier of unsupported type! "{type(self.curr_id)}"'
            )

    @property
    def slug(self):
        if isinstance(self.curr_id, str):
            return self.data_new[self.curr_id]["slug"]
        elif isinstance(self.curr_id, int):
            return self.data[self.curr_id]["slug"]
        else:
            raise Exception(
                f'NFT identifier of unsupported type! "{type(self.curr_id)}"'
            )

    @slug.setter
    def slug(self, value):
        if isinstance(self.curr_id, str):
            self.data_new[self.curr_id]["slug"] = str(value)
        elif isinstance(self.curr_id, int):
            self.data[self.curr_id]["slug"] = str(value)
        else:
            raise Exception(
                f'NFT identifier of unsupported type! "{type(self.curr_id)}"'
            )
