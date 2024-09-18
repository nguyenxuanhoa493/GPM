import requests
from dataclasses import dataclass

import conf


@dataclass(kw_only=True)
class Gpm:
    host: str = conf.gpm_host
    port: int = conf.gpm_port
    ver: int = conf.gpm_ver

    def __post_init__(self):
        self.api = f"http://{self.host}:{self.port}/api/v{self.ver}"
        self.check_status_running()
        self.profiles = self.get_list_profiles()

    def check_status_running(self) -> dict:
        is_running = self.send()
        if is_running == "GPM-Login":
            print(f"GPM is running in {self.api}")

    def send(self, url: str = "", payload: dict = {}) -> dict:
        url = f"{self.api}{url}"
        # print(url)
        try:
            response = requests.request("GET", url, params=payload)
        except:
            print(f"Kết nối không thành công đến: {url}")
            exit()

        if response.status_code != 200:
            print(f"Request failed with status code: {response.status_code}")
            return response.status_code

        try:
            return response.json()
        except ValueError:
            return response.text

    def get_list_profiles(
        self, group_id="", page=1, per_page=-1, sort=0, search=""
    ) -> list:
        """
        Get list of profiles from GPM.

        Args:
            group_id (str, optional): ID group cần lọc (lấy tại api Danh sách nhóm).
            page (int, optional): Số trang (mặc định 1).
            per_page (int, optional): Số profile mỗi trang (mặc định -1).
            sort (int, optional): 0 - Mới nhất, 1 - Cũ tới mới, 2 - Tên A-Z, 3 - Tên Z-A.
            search (str, optional): Từ khóa profile name.

        Returns:
            list: List of profiles.
        """
        payload = {
            "page": page,
            "per_page": per_page,
            "sort": sort,
        }
        if search:
            payload["search"] = search
        if group_id:
            payload["group_id"] = group_id
        response = self.send("/profiles", payload)
        return response.get("data", [])

    def get_detail_profile(self, profile_id: str) -> dict:
        """
        Get detail profile from GPM.

        Args:
            profile_id (int): ID profile.

        Returns:
            dict: Detail profile.
        """
        response = self.send(f"/profiles/{profile_id}")
        data = response.get("data", {})
        if data:
            return data
        else:
            print(f"Profile {profile_id} không tồn tại.")
            return {}

    def start_profile(
        self,
        profile_id: str,
        win_scale: float = 1,
        win_pos: str = "",
        win_size: str = "",
    ) -> dict:
        """
        Start a profile from GPM.

        Args:
            profile_id (str): ID profile.
            win_scale (float, optional): Giá trị từ 0 tới 1.0.
            win_pos (str, optional): Giá trị tọa độ trình duyệt theo dạng x,y.
            win_size (str, optional): Giá trị width,height.

        Returns:
            dict: Response from GPM.
        """
        payload = {"win_scale": win_scale, "win_pos": win_pos, "win_size": win_size}
        response = self.send(f"/profiles/start/{profile_id}", payload)
        if response["success"]:
            return response["data"]
        else:
            print(f"Profile {profile_id} {response['message']}.")
            return {}

    def close_profile(self, profile_id: str) -> bool:
        """
        Close a profile from GPM.

        Args:
            profile_id (str): ID profile.

        Returns:
            dict: Response from GPM.
        """
        response = self.send(f"/profiles/close/{profile_id}")
        if response["success"]:
            return True
        else:
            print(f"Profile {profile_id} {response['message']}.")
            return False
