"""Predict one image with the model selected by validation F1."""
import argparse,json
from pathlib import Path
from joblib import load
from experiment import ROOT,feature,LABELS

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('image');args=p.parse_args()
    summary=json.loads((ROOT/'results/summary.json').read_text(encoding='utf-8'))
    name=summary['selected_model']
    model=load(ROOT/f'models/{name.replace(" ","_")}.joblib')
    prediction=int(model.predict(feature(Path(args.image))[None,:])[0])
    print(json.dumps({'model':name,'label':prediction,'class':LABELS[prediction]},ensure_ascii=False))
