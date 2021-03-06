
import random
class HoneyWord(object):
    
    
    def __init__(self, n, size):
        [self.code, self.F_length, self.length] = self.train(n)
        [self.F_char, self.F_postfix]= self.F_post()
        self.size = size
        
        
    def train(self, num):
        count = 0;
        code = {}
        length_count={}
        F_length = {}
        for line in open("./rockyou-withcount.txt"):
            if count > num:
                break;
            n = 0;
            word = line.split(" ");
            while word[n] == '':
                n+=1;
            count += 1;
            code[word[n+1][:-1]] = int(word[n]);
            l = len(word[n+1])-1;
            if l in length_count:
                length_count[l] += int(word[n]);
            else:
                length_count[l] = int(word[n]);
        Sum = 0;
        for key in length_count:
            Sum += length_count[key]
        for key in length_count:
            F_length[key] = (length_count[key]+0.0)/Sum
        return [code, F_length, list(F_length.keys())]
    

    def decide_length(self, code):
        ##parameter : 0.3, with probability 0.3 that honeyword shares the same length with real password
        if random.random() < 0.3:
            d = len(code)
        else:
            c = random.random()
            f = 0;
            i = -1
            while c > f:
                i += 1
                f += self.F_length[self.length[i]]
            d = self.length[i]
        return d

    
    def F_post(self):
        Dic = {}
        char_count = {}
        F_postfix = {}
        code_key = list(self.code.keys())
        for string in code_key:
            i = 0;
            while i < len(string):
                if string[i] in char_count:
                    char_count[string[i]] += self.code[string]
                else:
                    char_count[string[i]] = self.code[string]
                if i < len(string)-1:
                    if string[i] not in Dic:
                        Dic[string[i]] = {}
                    if string[i+1] in Dic[string[i]]:
                        Dic[string[i]][string[i+1]] += self.code[string]
                    else:
                        Dic[string[i]][string[i+1]] = self.code[string]
                i += 1;
        Sum_char = 0;
        F_char = {};
        for char in char_count:
            Sum_char += char_count[char]
        for char in char_count:
            F_char[char] = (char_count[char]+0.0)/Sum_char
        for prefix in Dic:
            F_postfix[prefix] = {};
            Sum = 0;
            for postfix in Dic[prefix]:
                Sum += Dic[prefix][postfix]
            for postfix in Dic[prefix]:
                F_postfix[prefix][postfix] = (Dic[prefix][postfix]+0.0)/Sum        
        return [F_char, F_postfix]
    
    
    def generator(self, code):
        if code =='':
            ##parameter : "123456", just for now.
            code = '123456'
        result = [code]
        char_key = list(self.F_char.keys())
        for i in range(self.size):
            d = self.decide_length(code);
            ##parameter: 0.5 , which means 50% init char picked from real password
            if random.random() < 0.5:
                init = code[random.randint(0,len(code)-1)]
            else:
                c_init = random.random()
                f_init = 0
                i_init = -1
                while c_init > f_init:
                    i_init += 1
                    f_init += self.F_char[char_key[i_init]]
                init = char_key[i_init]
            honey = init
            temp = init;
            for j in range(d):
                ##parameter: 0.1, curing char picked from real password with probability 0.1
                if random.random() < 0.1:
                    honey += code[random.randint(0,len(code)-1)]
                else:
                    key = list(self.F_postfix[temp].keys())
                    c = random.random()
                    f = 0
                    i_within = -1
                    while c > f:
                        i_within += 1
                        f += self.F_postfix[temp][key[i_within]]
                    temp = key[i_within]
                    honey += key[i_within]
            result.append(honey)
        return result