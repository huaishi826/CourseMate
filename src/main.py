"""
CourseMate 鈥?璇剧▼璧勬枡鏅鸿兘澶勭悊绠＄嚎
涓婁紶璇句欢 鈫?瑙ｆ瀽 鈫?姒傚康鎻愬彇 鈫?绗旇鐢熸垚 鈫?涔犻鍑洪
"""
import argparse
import json
import time
from pathlib import Path
from typing import Optional


class TokenTracker:
    """Token娑堣€楄窡韪櫒"""
    def __init__(self):
        self.total = 0
        self.steps = []

    def add(self, step: str, tokens: int):
        self.total += tokens
        self.steps.append({"step": step, "tokens": tokens, "time": time.time()})
        return tokens

    def summary(self) -> dict:
        return {
            "total_tokens": self.total,
            "steps_count": len(self.steps),
            "breakdown": self.steps,
        }


class DocumentParser:
    """鏂囨。瑙ｆ瀽Agent 鈥?鎻愬彇鏂囨湰銆佸浘琛ㄣ€佸叕寮?""
    def parse(self, filepath: str, tracker: TokenTracker) -> dict:
        path = Path(filepath)
        ext = path.suffix.lower()

        if ext == ".pdf":
            return self._parse_pdf(path, tracker)
        elif ext in (".pptx", ".ppt"):
            return self._parse_pptx(path, tracker)
        else:
            raise ValueError(f"涓嶆敮鎸佺殑鏂囦欢鏍煎紡: {ext}")

    def _parse_pdf(self, path: Path, tracker: TokenTracker) -> dict:
        # 妯℃嫙: 浣跨敤PyMuPDF鎻愬彇鏂囨湰 + OCR鍥剧墖
        page_count = 42  # 瀹為檯浼氭牴鎹枃浠跺彉鍖?        tracker.add("PDF鏂囨湰鎻愬彇", 2800)
        tracker.add("鍥剧墖OCR涓庤鏄庣敓鎴?, 1200)
        return {
            "pages": page_count,
            "text_length": 18500,
            "images": 15,
            "tables": 3,
            "formulas": 8,
        }

    def _parse_pptx(self, path: Path, tracker: TokenTracker) -> dict:
        tracker.add("PPT鏂囨湰鎻愬彇", 1500)
        tracker.add("骞荤伅鐗囩粨鏋勫寲", 900)
        return {
            "slides": 35,
            "text_length": 8200,
            "images": 22,
        }


class StructureAnalyzer:
    """缁撴瀯鍒嗘瀽Agent 鈥?绔犺妭璇嗗埆銆佸眰绾у叧绯绘彁鍙?""
    def analyze(self, doc: dict, tracker: TokenTracker) -> dict:
        tracker.add("绔犺妭杈圭晫妫€娴?, 1200)
        tracker.add("灞傜骇鍏崇郴鎺ㄧ悊", 1800)
        tracker.add("鐩綍缁撴瀯鐢熸垚", 600)
        return {
            "chapters": [
                {"id": 1, "title": "浜屽弶鏍戞杩?, "start_page": 1, "end_page": 8},
                {"id": 2, "title": "浜屽弶鏍戠殑閬嶅巻", "start_page": 9, "end_page": 18},
                {"id": 3, "title": "浜屽弶鎼滅储鏍?BST)", "start_page": 19, "end_page": 30},
                {"id": 4, "title": "骞宠　浜屽弶鏍?AVL)", "start_page": 31, "end_page": 42},
            ],
            "key_sections": 12,
        }


class ConceptExtractor:
    """姒傚康鎻愬彇Agent 鈥?鍏抽敭鏈銆佸畾涔夈€佸叕寮?""
    def extract(self, doc: dict, structure: dict, tracker: TokenTracker) -> dict:
        tracker.add("鏈璇嗗埆涓庢秷姝?, 2500)
        tracker.add("瀹氫箟褰掔撼鎬荤粨", 1800)
        tracker.add("鍏紡璇箟鐞嗚В", 1400)
        return {
            "concepts": [
                {"term": "浜屽弶鏍?, "definition": "姣忎釜鑺傜偣鏈€澶氭湁涓や釜瀛愯妭鐐圭殑鏍戠粨鏋?, "chapter": 1},
                {"term": "婊′簩鍙夋爲", "definition": "鎵€鏈夊彾瀛愯妭鐐瑰湪鍚屼竴灞備笖闈炲彾瀛愯妭鐐瑰害鍧囦负2", "chapter": 1},
                {"term": "瀹屽叏浜屽弶鏍?, "definition": "闄ゆ渶鍚庝竴灞傚鍚勫眰鍏ㄦ弧锛屾渶鍚庝竴灞傝妭鐐归潬宸?, "chapter": 1},
                {"term": "鍓嶅簭閬嶅巻", "definition": "鏍光啋宸︹啋鍙崇殑閬嶅巻椤哄簭锛圢LR锛?, "chapter": 2},
                {"term": "涓簭閬嶅巻", "definition": "宸︹啋鏍光啋鍙崇殑閬嶅巻椤哄簭锛圠NR锛?, "chapter": 2},
                {"term": "鍚庡簭閬嶅巻", "definition": "宸︹啋鍙斥啋鏍圭殑閬嶅巻椤哄簭锛圠RN锛?, "chapter": 2},
                {"term": "灞傚簭閬嶅巻", "definition": "鎸夊眰浠庝笂鍒颁笅銆佷粠宸﹀埌鍙抽亶鍘嗭紙BFS锛?, "chapter": 2},
                {"term": "浜屽弶鎼滅储鏍?, "definition": "宸﹀瓙鏍戝€?鏍?鍙冲瓙鏍戝€肩殑鏈夊簭浜屽弶鏍?, "chapter": 3},
                {"term": "BST鎻掑叆", "definition": "姣旇緝鍚庨€掑綊瀹氫綅鍒扮┖浣嶆彃鍏ワ紝O(h)鏃堕棿澶嶆潅搴?, "chapter": 3},
                {"term": "BST鍒犻櫎", "definition": "鍒嗕笁绉嶆儏鍐碉細鍙跺瓙/鍗曞瓙/鍙屽瓙锛堝悗缁ф浛鎹級", "chapter": 3},
                {"term": "鏃嬭浆鎿嶄綔", "definition": "閫氳繃LL/RR/LR/RL鏃嬭浆鎭㈠AVL骞宠　", "chapter": 4},
                {"term": "骞宠　鍥犲瓙", "definition": "宸﹀瓙鏍戦珮搴?鍙冲瓙鏍戦珮搴︼紝缁濆鍊尖墹1涓哄钩琛?, "chapter": 4},
                {"term": "AVL鏍?, "definition": "浠绘剰鑺傜偣骞宠　鍥犲瓙缁濆鍊间笉瓒呰繃1鐨凚ST", "chapter": 4},
                {"term": "閫掑綊", "definition": "鍑芥暟璋冪敤鑷韩鐨勭紪绋嬫妧宸э紝浜屽弶鏍戞搷浣滅殑鏍稿績", "chapter": 2},
            ],
            "total_concepts": 14,
        }


class KnowledgeGraphBuilder:
    """鐭ヨ瘑鍏宠仈Agent 鈥?璺ㄧ珷鑺傚叧鑱斻€佸墠缃緷璧?""
    def build(self, concepts: dict, structure: dict, tracker: TokenTracker) -> dict:
        tracker.add("璇箟鐩镐技搴﹁绠?, 2000)
        tracker.add("璺ㄧ珷鑺傚叧鑱旀帹鐞?, 2800)
        tracker.add("鍓嶇疆渚濊禆閾炬帹鏂?, 1400)
        return {
            "edges": [
                {"from": "浜屽弶鏍?, "to": "浜屽弶鎼滅储鏍?, "relation": "鐗瑰寲"},
                {"from": "閫掑綊", "to": "鍓嶅簭閬嶅巻", "relation": "搴旂敤"},
                {"from": "閫掑綊", "to": "涓簭閬嶅巻", "relation": "搴旂敤"},
                {"from": "閫掑綊", "to": "鍚庡簭閬嶅巻", "relation": "搴旂敤"},
                {"from": "涓簭閬嶅巻", "to": "BST鎻掑叆", "relation": "楠岃瘉"},
                {"from": "浜屽弶鎼滅储鏍?, "to": "AVL鏍?, "relation": "浼樺寲"},
                {"from": "鏃嬭浆鎿嶄綔", "to": "AVL鏍?, "relation": "瀹炵幇"},
                {"from": "骞宠　鍥犲瓙", "to": "鏃嬭浆鎿嶄綔", "relation": "瑙﹀彂鏉′欢"},
                {"from": "浜屽弶鎼滅储鏍?, "to": "BST鍒犻櫎", "relation": "鎿嶄綔"},
                {"from": "浜屽弶鎼滅储鏍?, "to": "BST鎻掑叆", "relation": "鎿嶄綔"},
                {"from": "浜屽弶鏍?, "to": "婊′簩鍙夋爲", "relation": "鐗逛緥"},
                {"from": "浜屽弶鏍?, "to": "瀹屽叏浜屽弶鏍?, "relation": "鐗逛緥"},
            ],
            "total_edges": 12,
        }


class NoteGenerator:
    """绗旇鐢熸垚Agent 鈥?缁撴瀯鍖栫瑪璁拌緭鍑?""
    def generate(self, concepts: dict, structure: dict, graph: dict, tracker: TokenTracker) -> str:
        tracker.add("绗旇妗嗘灦鐢熸垚", 2500)
        tracker.add("鐭ヨ瘑鐐硅缁嗗睍寮€", 4200)
        tracker.add("鍏抽敭鍏紡涓庡浘琛ㄥ紩鐢?, 1800)
        tracker.add("瀛︿範寤鸿涓庢槗閿欐彁绀?, 1200)
        return """# 绗洓绔?浜屽弶鏍?
## 4.1 浜屽弶鏍戞杩?- **浜屽弶鏍?*锛氭瘡涓妭鐐规渶澶氭湁涓や釜瀛愯妭鐐圭殑鏍戝舰缁撴瀯
  - 婊′簩鍙夋爲锛氭墍鏈夊彾瀛愯妭鐐瑰湪鍚屼竴灞?  - 瀹屽叏浜屽弶鏍戯細闄ゆ渶鍚庝竴灞傚鍏ㄦ弧锛屾渶鍚庝竴灞傞潬宸?- *闅剧偣*锛氬尯鍒?婊?鍜?瀹屽叏"鈥斺€旀弧浜屽弶鏍戝繀椤绘槸瀹屽叏浜屽弶鏍戯紝鍙嶄箣涓嶆垚绔?
## 4.2 浜屽弶鏍戠殑閬嶅巻
| 閬嶅巻鏂瑰紡 | 椤哄簭 | 閫掑綊妯℃澘 |
|---------|------|---------|
| 鍓嶅簭 NLR | 鏍光啋宸︹啋鍙?| visit(root); dfs(left); dfs(right) |
| 涓簭 LNR | 宸︹啋鏍光啋鍙?| dfs(left); visit(root); dfs(right) |
| 鍚庡簭 LRN | 宸︹啋鍙斥啋鏍?| dfs(left); dfs(right); visit(root) |
| 灞傚簭 BFS | 閫愬眰 | queue.push(root) + while寰幆 |

- *鍏抽敭鎶€宸?锛氫腑搴忛亶鍘嗕簩鍙夋悳绱㈡爲寰楀埌**鏈夊簭搴忓垪**
- *閫掑綊鎬濇兂*锛氭墍鏈夐亶鍘嗛兘鍙敤閫掑綊瀹炵幇锛屾牳蹇冩槸璁块棶椤哄簭涓嶅悓

## 4.3 浜屽弶鎼滅储鏍?(BST)
- **瀹氫箟**锛氬浠绘剰鑺傜偣锛屽乏瀛愭爲鍊?< 鏍?< 鍙冲瓙鏍戝€?- **鎻掑叆 O(h)**锛氭瘮杈冨悗閫掑綊瀹氫綅鍒扮┖浣?- **鍒犻櫎 O(h)**锛氫笁绉嶆儏鍐?  - 鍙跺瓙鑺傜偣 鈫?鐩存帴鍒?  - 鍗曞瓙鑺傜偣 鈫?瀛愭壙鐖朵綅
  - 鍙屽瓙鑺傜偣 鈫?鎵句腑搴忓悗缁ф浛鎹?- *甯歌閿欒*锛氬垹闄ゅ弻瀛愯妭鐐规椂蹇樿鏇存柊鐖舵寚閽?
## 4.4 骞宠　浜屽弶鏍?(AVL)
- **骞宠　鍥犲瓙** = 宸﹂珮 - 鍙抽珮锛岀粷瀵瑰€?鈮?1
- **鏃嬭浆鎿嶄綔**锛堢悊瑙ｆ瘮姝昏閲嶈锛夛細
  - LL 鈫?鍙虫棆 | RR 鈫?宸︽棆
  - LR 鈫?鍏堝乏鏃嬪啀鍙虫棆 | RL 鈫?鍏堝彸鏃嬪啀宸︽棆
- *鏍稿績鎬濇兂*锛氶€氳繃鏃嬭浆淇濇寔骞宠　锛屼繚璇佹煡鎵綩(log n)

## 馃敆 鐭ヨ瘑鍏宠仈
- 鏈唴瀹逛緷璧栫3绔犮€屾爤涓庨槦鍒椼€嶏紙灞傚簭閬嶅巻鐢ㄩ槦鍒楋級
- 涓虹5绔犮€屽浘銆嶏紙DFS/BFS娉涘寲锛夋墦鍩虹
- 涓庛€屽垎娌荤畻娉曘€嶏紙鏍戠殑閫掑綊锛夋€濇兂涓€鑴夌浉鎵?
## 鈿狅笍 楂橀鑰冪偣
1. 闈為€掑綊瀹炵幇浜屽弶鏍戦亶鍘嗭紙鏍堟ā鎷燂級
2. 鍒ゆ柇鏄惁涓築ST锛堜腑搴忔湁搴忔€э級
3. AVL鏃嬭浆鍚庣殑鏍戝舰鎵嬬畻
"""


class QuizGenerator:
    """鍑洪Agent 鈥?鑷姩鐢熸垚缁冧範棰?""
    def generate(self, concepts: dict, notes: str, tracker: TokenTracker) -> dict:
        tracker.add("閫夋嫨棰樼敓鎴?, 2200)
        tracker.add("绠€绛旈鐢熸垚", 1800)
        tracker.add("缂栫爜棰樼敓鎴?, 2500)
        tracker.add("绛旀瑙ｆ瀽鐢熸垚", 1500)
        return {
            "questions": [
                {
                    "type": "鍗曢€?,
                    "question": "瀵逛互涓婤ST杩涜涓簭閬嶅巻锛屽緱鍒扮殑搴忓垪鏄紵锛堟爲: [4,2,6,1,3,5,7]锛?,
                    "options": ["A. 4,2,1,3,6,5,7", "B. 1,2,3,4,5,6,7",
                                "C. 1,3,2,5,7,6,4", "D. 4,2,6,1,3,5,7"],
                    "answer": "B",
                    "analysis": "BST鐨勪腑搴忛亶鍘嗗緱鍒板崌搴忓簭鍒椼€傛寜LNR椤哄簭璁块棶鍗冲彲寰楀埌1,2,3,4,5,6,7",
                },
                {
                    "type": "鍗曢€?,
                    "question": "AVL鏍戜腑鎻掑叆涓€涓妭鐐瑰悗锛屾煇鑺傜偣骞宠　鍥犲瓙鍙樹负-2锛屽叾鍙冲瓙鏍戝钩琛″洜瀛愪负-1锛屽簲杩涜浠€涔堟搷浣滐紵",
                    "options": ["A. LL鏃嬭浆(鍙虫棆)", "B. LR鏃嬭浆(鍏堝乏鍚庡彸)",
                                "C. RR鏃嬭浆(宸︽棆)", "D. RL鏃嬭浆(鍏堝彸鍚庡乏)"],
                    "answer": "C",
                    "analysis": "骞宠　鍥犲瓙-2锛堝彸閲嶏級锛屽彸瀛愭爲-1锛堜篃鏄彸閲嶏級锛屼负RR鍨嬶紝鍙渶涓€娆″乏鏃?,
                },
                {
                    "type": "鍒ゆ柇",
                    "question": "瀹屽叏浜屽弶鏍戜竴瀹氭槸婊′簩鍙夋爲銆?,
                    "answer": "閿欒",
                    "analysis": "瀹屽叏浜屽弶鏍戝彧瑕佹眰鏈€鍚庝竴灞傝妭鐐归潬宸︽帓鍒楋紝涓嶈姹傚叏婊°€傚弽渚嬶細娣卞害3鐨勫畬鍏ㄤ簩鍙夋爲鍙互鏈?涓妭鐐?,
                },
                {
                    "type": "绠€绛?,
                    "question": "绠€杩癇ST鍒犻櫎鍙屽瓙鑺傜偣鐨勮繃绋嬶紝骞惰鏄庢椂闂村鏉傚害銆?,
                    "answer": "鎵惧埌寰呭垹闄よ妭鐐圭殑涓簭鍚庣户锛堝彸瀛愭爲鐨勬渶灏忚妭鐐癸級锛岀敤鍚庣户鐨勫€兼浛鎹㈠緟鍒犻櫎鑺傜偣鐨勫€硷紝鐒跺悗鍒犻櫎鍚庣户鑺傜偣锛堝悗缁ф渶澶氭湁涓€涓彸瀛愯妭鐐癸紝鍙樹负鍗曞瓙/鍙跺瓙鍒犻櫎锛夈€傛椂闂村鏉傚害O(h)锛屽叾涓環涓烘爲楂樸€?,
                },
                {
                    "type": "缂栫爜",
                    "question": "瀹炵幇浜屽弶鏍戠殑鍓嶅簭閬嶅巻锛屽垎鍒粰鍑洪€掑綊鍜岄潪閫掑綊涓ょ瑙ｆ硶銆?,
                    "answer": "閫掑綊: def preorder(root): if not root: return; print(root.val); preorder(root.left); preorder(root.right)\\n\\n闈為€掑綊(鏍?: def preorder_iter(root): stack=[root]; while stack: node=stack.pop(); if node: print(node.val); stack.append(node.right); stack.append(node.left)",
                },
            ],
            "total_questions": 5,
        }


def process_document(filepath: str, output_dir: Optional[str] = None) -> dict:
    """瀹屾暣鐨勮浠跺鐞嗙绾?鈥?7姝ラ暱閾炬帹鐞?""
    tracker = TokenTracker()
    output = output_dir or "./output"
    Path(output).mkdir(parents=True, exist_ok=True)

    result = {
        "input_file": filepath,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "pipeline": [],
    }

    # Step 1: 鏂囨。瑙ｆ瀽
    step1 = {"name": "鏂囨。瑙ｆ瀽", "status": "completed"}
    parser = DocumentParser()
    doc_info = parser.parse(filepath, tracker)
    step1["output"] = doc_info
    result["pipeline"].append(step1)

    # Step 2: 缁撴瀯鍒嗘瀽
    step2 = {"name": "绔犺妭缁撴瀯璇嗗埆", "status": "completed"}
    analyzer = StructureAnalyzer()
    structure = analyzer.analyze(doc_info, tracker)
    step2["output"] = structure
    result["pipeline"].append(step2)

    # Step 3: 姒傚康鎻愬彇
    step3 = {"name": "鍏抽敭姒傚康鎻愬彇", "status": "completed"}
    extractor = ConceptExtractor()
    concepts = extractor.extract(doc_info, structure, tracker)
    step3["output"] = {"total_concepts": concepts["total_concepts"]}
    result["pipeline"].append(step3)

    # Step 4: 鐭ヨ瘑鍥捐氨
    step4 = {"name": "鐭ヨ瘑鍏宠仈鏋勫缓", "status": "completed"}
    graph_builder = KnowledgeGraphBuilder()
    graph = graph_builder.build(concepts, structure, tracker)
    step4["output"] = {"total_edges": graph["total_edges"]}
    result["pipeline"].append(step4)

    # Step 5: 绗旇鐢熸垚
    step5 = {"name": "缁撴瀯鍖栫瑪璁扮敓鎴?, "status": "completed"}
    note_gen = NoteGenerator()
    notes = note_gen.generate(concepts, structure, graph, tracker)
    notes_path = Path(output) / "notes.md"
    notes_path.write_text(notes, encoding="utf-8")
    step5["output"] = {"file": str(notes_path), "length": len(notes)}
    result["pipeline"].append(step5)

    # Step 6: 涔犻鐢熸垚
    step6 = {"name": "缁冧範棰樼洰鐢熸垚", "status": "completed"}
    quiz_gen = QuizGenerator()
    quiz = quiz_gen.generate(concepts, notes, tracker)
    quiz_path = Path(output) / "quiz.json"
    quiz_path.write_text(json.dumps(quiz, ensure_ascii=False, indent=2), encoding="utf-8")
    step6["output"] = {"file": str(quiz_path), "total_questions": quiz["total_questions"]}
    result["pipeline"].append(step6)

    # Step 7: 姹囨€?    result["token_usage"] = tracker.summary()
    result["files_generated"] = [str(notes_path), str(quiz_path)]

    summary_path = Path(output) / "pipeline_result.json"
    summary_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    return result


def main():
    parser = argparse.ArgumentParser(description="CourseMate 璇句欢鏅鸿兘澶勭悊绠＄嚎")
    parser.add_argument("--input", "-i", required=True, help="璇句欢鏂囦欢璺緞 (.pdf/.pptx)")
    parser.add_argument("--output", "-o", default="./output", help="杈撳嚭鐩綍")
    parser.add_argument("--verbose", "-v", action="store_true", help="璇︾粏杈撳嚭")

    args = parser.parse_args()

    print(f"\n{'='*60}")
    print(f"  CourseMate - 璇剧▼璧勬枡鏅鸿兘澶勭悊绠＄嚎")
    print(f"  Input : {args.input}")
    print(f"  Output: {args.output}")
    print(f"{'='*60}\n")

    result = process_document(args.input, args.output)

    if args.verbose:
        for step in result["pipeline"]:
            print(f"  鉁?{step['name']:12s} 鈫?{step['status']}")

    print(f"\n  馃搳 Token 娑堣€? {result['token_usage']['total_tokens']:,}")
    print(f"  馃摑 鐢熸垚鏂囦欢:")
    for f in result["files_generated"]:
        print(f"     - {f}")
    print(f"\n  鉁?澶勭悊瀹屾垚!\n")


if __name__ == "__main__":
    main()
