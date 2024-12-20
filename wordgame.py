import pypinyin
import random
from wordbase import WORD_DATABASE

class WordChainGame:
    def __init__(self):
        self.used_words = set()
        self.previous_word = ""
        self.player_score = 0
        self.computer_score = 0

    def get_pinyin_full(self, char):
        """获取字的完整拼音"""
        return pypinyin.lazy_pinyin(char)[0]

    def get_computer_word(self, last_char):
        """电脑根据上一个字选择下一个词"""
        last_char_pinyin = self.get_pinyin_full(last_char)
        
        # 遍历所有词库寻找合适的词
        all_available_words = []
        for words in WORD_DATABASE.values():
            for word in words:
                if word not in self.used_words:
                    first_char_pinyin = self.get_pinyin_full(word[0])
                    if first_char_pinyin == last_char_pinyin:
                        all_available_words.append(word)
    
        if all_available_words:
            return random.choice(all_available_words)
        return None

    def is_valid_word(self, word):
        """检查输入是否为有效的中文词语"""
        if len(word) < 2:
            return False
        for char in word:
            if not '\u4e00' <= char <= '\u9fff':
                return False
        return True

    def check_word_match(self, word):
        """检查词语是否符合接龙规则"""
        if not self.previous_word:
            return True
        
        last_char_pinyin = self.get_pinyin_full(self.previous_word[-1])
        first_char_pinyin = self.get_pinyin_full(word[0])
        return last_char_pinyin == first_char_pinyin

    def play(self):
        print("\n欢迎玩词语接龙游戏！")
        print("规则：")
        print("1. 输入的词语必须以上一个词的最后一个字（或同音字）开头")
        print("2. 不能重复使用已经用过的词")
        print("3. 输入'退出'结束游戏")
        print("4. 每成功接龙一次得1分\n")

        while True:
            # 玩家回合
            if not self.previous_word:
                user_input = input("请输入一个词语开始游戏：")
            else:
                last_char = self.previous_word[-1]
                last_pinyin = self.get_pinyin_full(last_char)
                user_input = input(f"请输入一个以'{last_char}'(拼音：{last_pinyin})或其同音字开头的词语：")
            
            # 检查是否退出
            if user_input == "退出":
                self.show_final_score()
                break
            
            # 验证输入
            if not self.is_valid_word(user_input):
                print("请输入有效的中文词语！")
                continue
            
            if user_input in self.used_words:
                print("这个词已经用过了，请换一个！")
                continue
            
            if not self.check_word_match(user_input):
                last_char = self.previous_word[-1]
                last_pinyin = self.get_pinyin_full(last_char)
                print(f"输入错误！必须以'{last_char}'(拼音：{last_pinyin})或同音字开头！")
                continue
            
            # 玩家回合成功
            self.used_words.add(user_input)
            self.previous_word = user_input
            self.player_score += 1
            print(f"你的词语：{user_input}")
            print(f"当前比分 - 你：{self.player_score} 电脑：{self.computer_score}")
            
            # 电脑回合
            computer_word = self.get_computer_word(user_input[-1])
            if computer_word:
                print(f"电脑的词语：{computer_word}")
                self.used_words.add(computer_word)
                self.previous_word = computer_word
                self.computer_score += 1
                print(f"当前比分 - 你：{self.player_score} 电脑：{self.computer_score}")
            else:
                print("\n电脑想不出词了，你赢了！")
                self.show_final_score()
                break

    def show_final_score(self):
        """显示最终得分"""
        print("\n游戏结束！")
        print(f"最终比分 - 你：{self.player_score} 电脑：{self.computer_score}")
        if self.player_score > self.computer_score:
            print("恭喜你获胜！")
        elif self.player_score < self.computer_score:
            print("电脑获胜！")
        else:
            print("平局！")

def main():
    # 确保已安装pypinyin
    try:
        import pypinyin
    except ImportError:
        print("请先安装pypinyin库：")
        print("pip install pypinyin")
        return

    game = WordChainGame()
    game.play()

if __name__ == "__main__":
    main()
