import os
import csv

from typing import Optional, List
from collections import Counter
from dataclasses import dataclass


@dataclass
class AssembleParticipant:
    id: str
    first_name: str
    last_name: str
    phone_number: str
    email: str
    affiliated_church: str
    title_in_church: str
    workshop_saturday_am: str
    workshop_saturday_pm: str
    need_accomendation: str
    need_children_care: str
    children_care_number: str
    tshirt_size: str
    need_saturday_tour_guide: str
    need_lunch_sunday: str
    zone_or_group_name: Optional[str] = None
    chinese_name: Optional[str] = None
    other_questions: Optional[str] = None
    promo_code: Optional[str] = None
    emergency_contact: Optional[str] = None
    need_dinner_friday: Optional[str] = None
    payment_info: Optional[str] = None


EMAIL_TEMPLATE = """<html><body>
親愛的靈糧家人 {first_name} {last_name},<br><br>
    馬上就是北美靈糧青年特會
    <a href="https://rolcc.net/rolcc2/assemble2024/">Assemble2024</a>啦🎉!
    <br><br>
    在大家出發前，有一些重要的注意事項和備忘，請仔細閱讀附件的<b>PDF特會手冊</b>並做好準備。<br><br>
    以下是你的<b><u>重要註冊信息</u></b>，
    <b>請確保mark這封email。在進行註冊時，請提供同工你的<u>報名序號</u></b>。
    <br><br>
    &emsp; 報名序號: <b>{id}</b><br>
    &emsp; T-shirt size: <b>{tshirt_size}</b><br>
    &emsp; Assemble 專題講座 (週六上午): <b>{workshop_saturday_am}</b>, 教室: <b>{workshop_saturday_am_room}</b><br>
    &emsp; Assemble 專題講座 (週六下午): <b>{workshop_saturday_pm}</b>, 教室: <b>{workshop_saturday_pm_room}</b><br>
    &emsp; 9/27週五是否有代訂便當 : <b>{need_dinner_friday}</b><br>
    &emsp; 9/28週六下午是否參加生命河靈糧堂事工導覽 : <b>{need_saturday_tour_guide}</b><br>
    &emsp; 9/29週日是否需要午餐 : <b>{need_lunch_sunday}</b><br>
    <br>
我們期待9月27日在生命河與你相會！
<br><br>
主內，<br>
矽谷生命河靈糧堂Assemble全體同工&牧者團隊
</body></html>
"""

WORKSHOP_ROOM = {
    # AM
    "跳脫傳統——AI時代的事奉": "C1",
    "先知性預言與禱告訓練": "F1",
    "吃喝玩樂中提升教會士氣": "G11",
    "恢復事奉中的喜樂與滿足": "G10",
    "培育下一代的領袖同工" : "F2",
    # PM
    "學生事工": "E5",
    "弟兄事工": "G5",
    "姐妹事工": "G6",
    "家庭事奉": "Y2",
    "敬拜讚美": "G11",
    "小組教會": "F2",
    "靈力事奉": "G10",
    "職場宣教": "K4",
}

def find_workshop_room(workshop_name: str) -> str:
    for k, v in WORKSHOP_ROOM.items():
        if workshop_name.startswith(k):
            return v
    return ""

def parse_assemble_registration_csv_file(input_file: str) -> List[AssembleParticipant]:
    participants: List[AssembleParticipant] = []

    def empty_to_none(input: str):
        return None if input == "" else input

    with open(input_file, "r", encoding="utf-8") as fid:
        reader = csv.reader(fid)
        for i, row in enumerate(reader):
            if i < 2:
                # titles are in the 1st 2 rows
                continue
            if row[1] == "" and row[2] == "":
                # skip empty first and last name
                continue

            participants.append(
                AssembleParticipant(
                    id=row[0],
                    first_name=row[1].replace(" ", ""),
                    last_name=row[2].replace(" ", ""),
                    chinese_name=empty_to_none(row[3]),
                    phone_number=row[4],
                    email=row[5],
                    affiliated_church=row[6],
                    title_in_church=row[7],
                    zone_or_group_name=row[8],
                    workshop_saturday_am=row[9],
                    workshop_saturday_pm=row[10],
                    need_accomendation=empty_to_none(row[11]),
                    need_children_care=empty_to_none(row[12]),
                    children_care_number=empty_to_none(row[13]),
                    tshirt_size=row[14],
                    need_saturday_tour_guide=row[15],
                    need_lunch_sunday=row[16],
                    other_questions=empty_to_none(row[17]),
                    emergency_contact=empty_to_none(row[18]),
                    promo_code=empty_to_none(row[19]),
                    need_dinner_friday=row[20],
                    payment_info=empty_to_none(row[21]),
                )
            )
    return participants


class AssembleDataset:
    participants: List[AssembleParticipant]

    def __init__(self, dataset_csv_file: str) -> None:
        if not os.path.exists(dataset_csv_file):
            raise ValueError(f"Error: dataset file not found: {dataset_csv_file}")

        self.participants = parse_assemble_registration_csv_file(dataset_csv_file)
        print(
            f"Parsed csv file:{dataset_csv_file}\nParticipant number: {len(self.participants)}\n"
        )

    def compose_single_email(self, person: AssembleParticipant) -> str:
        return EMAIL_TEMPLATE.format(
            first_name=person.first_name,
            last_name=person.last_name,
            id=person.id.zfill(3),
            tshirt_size=person.tshirt_size,
            workshop_saturday_am=person.workshop_saturday_am,
            workshop_saturday_pm=person.workshop_saturday_pm,
            workshop_saturday_am_room=find_workshop_room(person.workshop_saturday_am),
            workshop_saturday_pm_room=find_workshop_room(person.workshop_saturday_pm),
            need_dinner_friday=(
                person.need_dinner_friday
                if person.need_dinner_friday not in ["不需代訂", ""]
                else "否"
            ),
            need_saturday_tour_guide=person.need_saturday_tour_guide,
            need_lunch_sunday=person.need_lunch_sunday,
        )

    def print_stats(self):
        unique_id = set()
        for p in self.participants:
            unique_id.add(p.id)
        print(f"Unique IDs: {len(unique_id)}")
