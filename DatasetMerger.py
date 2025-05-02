import os
import shutil

# Konfigurasi
class_map = {
    "helm": 0,
    "rompi": 1,
    "sarung_tangan": 2,
    "sepatu": 3
}

splits = ["train", "valid", "test"]
base_input = "C:\\Users\\ACER\\Videos\\tes"
base_output = "C:\\Users\\ACER\\Videos\\output"

# Buat folder output
for split in splits:
    os.makedirs(os.path.join(base_output, "images", split), exist_ok=True)
    os.makedirs(os.path.join(base_output, "labels", split), exist_ok=True)

# Proses tiap alat dan split
for alat, class_id in class_map.items():
    for split in splits:
        image_dir = os.path.join(base_input, alat, split, "images")
        label_dir = os.path.join(base_input, alat, split, "labels")

        for label_file in os.listdir(label_dir):
            if not label_file.endswith(".txt"):
                continue

            # Baca dan ubah class ID
            with open(os.path.join(label_dir, label_file), "r") as f:
                lines = f.readlines()

            new_lines = []
            for line in lines:
                parts = line.strip().split()
                if len(parts) < 5:
                    continue
                parts[0] = str(class_id)
                new_lines.append(" ".join(parts))

            # Simpan label baru
            label_out_path = os.path.join(base_output, "labels", split, label_file)
            with open(label_out_path, "w") as f:
                f.write("\n".join(new_lines))

            # Copy image
            image_name = label_file.replace(".txt", ".jpg")  # atau .png jika perlu
            image_src_path = os.path.join(image_dir, image_name)
            image_dst_path = os.path.join(base_output, "images", split, image_name)

            if os.path.exists(image_src_path):
                shutil.copy(image_src_path, image_dst_path)