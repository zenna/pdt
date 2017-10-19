from benchmarks.clevr.clevr import questions_iter, scenes_iter, SceneGraph, interpret

def test_interpret():
  qitr = questions_iter()
  sitr = scenes_iter()

  for i in range(100):
    s1 = next(sitr)
    # 10 questions per scene it seems
    for i in range(10):
      q1 = next(qitr)
      scene = SceneGraph.from_json(s1)
      res = interpret(q1['program'], scene.object_set, scene.relations)
      print(res, q1['answer'])
