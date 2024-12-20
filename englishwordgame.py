import time
import random
from collections import defaultdict

class WordChainGame:
    def __init__(self):
        # 简单的词库,实际使用时可以导入更大的词库
        self.word_dict = {'apple', 'elephant', 'teacher', 'rabbit', 'tree', 'eagle', 
                         'example', 'yellow', 'window', 'water', 'rain', 'nice',
                         'queen', 'zebra', 'xylophone'}
        self.used_words = set()  # 记录已使用的单词
        self.players = {}  # 记录玩家分数
        self.difficult_letters = {'q', 'x', 'z'}
        
    def initialize_game(self):
        """初始化游戏"""
        n = int(input("请输入玩家数量: "))
        for i in range(n):
            name = input(f"请输入玩家{i+1}的名字: ")
            self.players[name] = 0
        print("\n游戏开始!")
        return list(self.players.keys())

    def is_valid_word(self, word, last_word):
        """检查单词是否有效"""
        if len(word) < 3:
            print("单词长度必须至少为3个字母!")
            return False
            
        if word in self.used_words:
            print("该单词已被使用!")
            return False
            
        if word not in self.word_dict:
            print("该单词不在词库中!")
            return False
            
        if last_word and word[0] != last_word[-1]:
            print(f"单词必须以字母 {last_word[-1]} 开头!")
            return False
            
        return True

    def calculate_score(self, word):
        """计算得分"""
        score = 1  # 基础分
        if len(word) >= 8:
            score += 1  # 长单词额外分
        if word[0] in self.difficult_letters:
            score += 2  # 困难字母额外分
        return score

    def play_turn(self, player, last_word):
        """玩家回合"""
        print(f"\n{player}的回合")
        print(f"请说出一个以 '{last_word[-1] if last_word else '任意字母'}' 开头的单词")
        
        start_time = time.time()
        word = input("你的单词: ").lower()
        end_time = time.time()
        
        if end_time - start_time > 60:
            print("超时!")
            return None
            
        if self.is_valid_word(word, last_word):
            self.used_words.add(word)
            score = self.calculate_score(word)
            self.players[player] += score
            print(f"得分: +{score}")
            return word
        return None

    def play_game(self):
        """运行游戏"""
        players = self.initialize_game()
        current_word = ""
        active_players = players.copy()
        
        while len(active_players) > 1:
            for player in players[:]:
                if player not in active_players:
                    continue
                    
                result = self.play_turn(player, current_word)
                if result:
                    current_word = result
                    print(f"\n当前得分: ")
                    for p, score in self.players.items():
                        print(f"{p}: {score}")
                else:
                    print(f"{player} 被淘汰!")
                    active_players.remove(player)
                    if len(active_players) == 1:
                        break
                        
        winner = active_players[0]
        print(f"\n游戏结束! 获胜者是 {winner}, 得分: {self.players[winner]}")

if __name__ == "__main__":
    game = WordChainGame()
    game.play_game()
