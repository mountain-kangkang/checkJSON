import os
import shutil as sh
import json
from pathlib import Path

current_path = Path(os.getcwd())

hidden_path = [h for r in current_path.iterdir() if r.is_dir() for h in list(r.glob('**/*.DS_Store'))]
image_path = [i for a in current_path.iterdir() if a.is_dir() for i in list(a.glob('**/*.png.json'))]
calib_path = [c for b in current_path.iterdir() if b.is_dir() for c in list(b.glob('**/*.png.json.json'))]
ann_path = [an for d in current_path.iterdir() if d.is_dir() for an in list(d.glob('**/*.pcd.json'))]
png_path = [p for e in current_path.iterdir() if e.is_dir() for p in list(e.glob('**/*.png'))]
data_path = [r for r in current_path.iterdir() if r.is_dir()]

#print(image_path)
#print(calib_path)

png_temp = []

for png in png_path:
  png_temp.append(str(png.parent).split('/')[-1][:-4])
print(png_temp)

for image in image_path:
  img_temp = str(image.parent).split('/')[-1][:-4]
  print(img_temp)
  if img_temp not in png_temp:
    image.rename(Path(os.path.join(str(image.parent), f'{img_temp}.png')).as_posix())

for calib in calib_path:
  cal_temp = str(calib.parent).split('/')[-1][:-4]
  calib.rename(Path(os.path.join(str(calib.parent), f'{cal_temp}.png.json')).as_posix())


new_calib_path = [nc for a in current_path.iterdir() if a.is_dir() for nc in list(a.glob('**/*.png.json'))]

for cal in new_calib_path:
  new_temp = str(cal.parent).split('/')[-1][:-4]
  with open(cal, 'r') as cf:
    calib_json = json.load(cf)
  
  calib_json['name'] = f'{new_temp}.png'

  del(calib_json['pathOriginal'])
  del(calib_json['id'])
  del(calib_json['entityId'])
  del(calib_json['createdAt'])
  del(calib_json['updatedAt'])
  del(calib_json['fileMeta'])
  del(calib_json['preview'])
  del(calib_json['fullStorageUrl'])
  
  with open(cal, 'w', encoding='utf-8') as ncf:
    json.dump(calib_json, ncf, ensure_ascii=False, indent='\t')


for hidden_file in hidden_path:
  os.remove(hidden_file)

remove_ann = []

for ann in ann_path:
  with open(ann, 'r') as af:
    ann_json = json.load(af)
        
  if len(ann_json['figures']) == 0:
    remove_ann.append(str(ann).split('/')[-1][:-9])


for data in data_path:
  data_folder = [df for d in data.iterdir() if d.is_dir() for df in d.iterdir() if df.is_dir()]
  #print(data_folder)
  #print(remove_ann)

  for ran in remove_ann:
    for folder in data_folder:
      # remove ann
      try:
        os.remove(Path(folder/'ann'/f'{ran}.pcd.json'))
      except:
        pass
        
      # remove pcd
      try:
        os.remove(Path(folder/'pointcloud'/f'{ran}.pcd'))
      except:
        pass
        
      # remove image
      try:
        sh.rmtree(Path(folder/'related_images'/f'{ran}_pcd'))
      except:
        pass
  
  print(f'{data} 변환 완료')
