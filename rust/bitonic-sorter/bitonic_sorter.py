"Bitonic Merge Sortモジュール"

def sort(x, up):
  """リストxの要素をupで指定された向きにソートする
  upがTrueなら昇順にソートし、Falseなら降順になる
  xの要素数は2のべき乗でなければならない
  (さもなければソート結果がおかしくなる)
  """
  if len(x) <= 1:
    return x
  else:
    # step 1a
    # xを前半と後半に分け、前半は昇順、後半は降順にソートする
    mid_point = len(x) // 2
    first = sort(x[:mid_point], True)
    second = sort(x[mid_point:], False)

    # step 1b
    # ２分割したリストを1つに結合する
    x1 = first + second

    # step 2
    # subsortに渡す
    return _subsort(x1, up)
  
def _subsort(x: list[int], up: bool)->list[int]:
  """
  バイトニックにソートされたリストxの前半と後半を、upで指定された向きに
  比較、交換し、前半と後半それぞれについて再起的にサブソートを適用する
  """
  if len(x) == 1:
    return x
  else:
    # step 2a
    # 要素数nのバイトニック列を、n/2要素おきに比較して、
    # upで指定された向き(昇順ならup=True)になるよう交換する
    _compare_and_swap(x, up)

    # step 2b
    # データ列を半分に分割し、それぞれに対して_subsortを再帰的に適用する
    mid_point = len(x) // 2
    first = _subsort(x[:mid_point], up)
    second = _subsort(x[mid_point:], up)
    return first + second

def _compare_and_swap(x: list[int], up: bool):
  """
  要素数nのバイトニック列を、n/2要素おきに比較して、
  upで指定された向き(昇順ならup=True)になるよう交換する
  """
  mid_point = len(x) // 2
  for i in range(mid_point):
    if (x[i] > x[mid_point + i]) is up:
      # 要素を交換する
      x[i], x[mid_point + i] = x[mid_point + i], x[i]

if __name__ == '__main__':
  import random
  x = [random.randint(0, 1000) for _ in range(32)]
  print(x)
  print(sort(x, True))