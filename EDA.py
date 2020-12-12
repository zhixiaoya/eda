# import macropodus
import synonyms
import random
import jieba


KEY_WORDS = ["macropodus"] # ���滻ͬ��ʵĴ���
ENGLISH = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


def is_english(text):
    """
        �Ƿ�ȫ��Ӣ��
    :param text: str, like "����˭"
    :return: boolean, True or False
    """
    try:
        text_r = text.replace(" ", "").strip()
        for tr in text_r:
            if tr in ENGLISH:
                continue
            else:
                return False
    except Exception as e:
        return False


def is_number(text):
    """
        �ж�һ���Ƿ�ȫ�ǰ���������
    :param text: str, like "1001"
    :return: boolean, True or False 
    """
    try:
        text_r = text.replace(" ", "").strip()
        for tr in text_r:
            if tr.isdigit():
                continue
            else:
                return False
    except Exception as e:
        return False


def get_syn_word(word):
    """
        ��ȡͬ���
    :param word: str, like "ѧ��"
    :return: str, like "ѧ����"
    """
    if not is_number(word.strip()) or not is_english(word.strip()):
        word_syn = synonyms.nearby(word)
        word_syn = word_syn[0] if len(word_syn[0]) else [word]
        return word_syn
    else:
        return [word]


def syn_replace(words, n=1):
    """
        ͬ����滻
    :param words: list, like ["macropodus", "��", "˭"]
    :param n: int, like 128
    :return: list, like ["macropodus", "�ǲ���", "�ĸ�"]
    """
    words_set = list(set(words)) # ����, ѡ��
    random.shuffle(words_set)
    count = 0
    for ws in words_set:
        if ws in KEY_WORDS or is_english(ws) or is_number(ws):
            continue  # �ؼ���/Ӣ��/���������ֲ��滻
        need_words = get_syn_word(ws) # ��ȡͬ���(�����ж��)
        if need_words: # �����ͬ������滻
            need_words = random.choice(need_words)
            words = [need_words if w==ws else w for w in words]
            count += 1
        if count >= n:
            break
    return words


def syn_insert(words, n=1, use_syn=True):
    """
        ͬ����滻
    :param words: list, like ["macropodus", "��", "˭"]
    :param n: int, like 32
    :return: list, like ["macropodus", "�ǲ���", "�ĸ�"]
    """
    words_set = list(set(words))  # ����, ѡ��
    random.shuffle(words_set)
    count = 0
    for ws in words_set:
        if ws in KEY_WORDS or is_english(ws) or is_number(ws):
            continue  # �ؼ���/Ӣ��/���������ֲ��滻
        if use_syn:
            need_words = get_syn_word(ws)  # ��ȡͬ���(�����ж��)
        else:
            need_words = [ws]
        if need_words:  # �����ͬ������滻
            random_idx = random.randint(0, len(words) - 1)
            words.insert(random_idx, (need_words[0]))
            count += 1
        if count >= n:
            break
    return words


def word_swap(words, n=1):
    """
        ������������������������
    :param words: list, like ["macropodus", "��", "˭"]
    :param n: int, like 2
    :return: list, like ["macropodus", "˭", "��"]
    """
    idxs = [i for i in range(len(words))]
    count = 0
    while count < n:
        idx_select = random.sample(idxs, 2)
        temp = words[idx_select[0]]
        words[idx_select[0]] = words[idx_select[1]]
        words[idx_select[1]] = temp
        count += 1
    return words


def word_delete(words, n=1):
    """
        ���ɾ��N������
    :param words: list, like ["macropodus", "��", "˭"]
    :param n: int, like 1
    :return: list, like ["macropodus", "˭"]
    """
    count = 0
    while count < n:
        word_choice = random.choice(words)
        if word_choice not in KEY_WORDS:
            words.remove(word_choice)
            count += 1
    return words


def word_cut(text, tool="macropodus"):
    """
        �дʹ���
    :param text:str, like "macropodus��˭" 
    :param tool: str, "macropodus" or "jieba"
    :return: list, like ["macropodus", "��", "˭"]
    """
    if tool=="macropodus":
        text_cut = list(macropodus.cut(text))
    elif tool=="jieba":
        text_cut = list(jieba.cut(text))
    else:
        text_cut = list(jieba.cut(text))
    return text_cut


def eda(text, n=1, use_syn=True):
    """
        EDA, ÿ�ַ�����һλ
    :param text: str, like "macropodus��˭" 
    :param n: int, like 1
    :param use_syn: Boolean, True or False
    :return: list, like ["macropodus��˭ѽ", "macropodus��"]
    """
    sens = word_cut(text, tool="jieba")
    # print(sens)
    sr = syn_replace(sens.copy(), n=n)
    si = syn_insert(sens.copy(), n=n, use_syn=use_syn)
    ws = word_swap(sens.copy(), n=n)
    wd = word_delete(sens.copy(), n=n)
    sens_word_4 = [sr, si, ws, wd]
    # print(sens_word_4)
    sens_4 = ["".join(s4) for s4 in sens_word_4]
    return sens_4


if __name__ == "__main__":
    sens = "".join(["macropodus", "�ǲ���", "�ĸ�", "����",
                    "ֻ���������ĵ㣬���������������ÿ�ȫ�껨�����ϣ�"])
    print(eda(sens))


    sens = list(sens)
    res1 = syn_replace(sens, n=1)
    print(res1)
    res2 = syn_insert(sens.copy(), n=1, use_syn=True)
    print(res2)
    res3 = word_swap(sens.copy(), n=1)
    print(res3)
    res4 = word_delete(sens.copy(), n=1)
    print(res4)