import re
from pathlib import Path
import os
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
from tqdm import tqdm

main_path = os.path.dirname(os.path.realpath(__file__))


def norm_path(s: str):
    return re.sub(r'[^\w\-_\. ]', '_', s)


def get_groups(a, n):
    return [
        a[i * n:(i + 1) * n]
        for i in range(len(a))
        if a[i * n:(i + 1) * n]
    ]


def merge_images(figures):
    all_imgs = [
        Image.frombytes(
            'RGB',
            fig.canvas.get_width_height(), fig.canvas.tostring_rgb())
        for fig in figures
    ]

    imgs_groups = get_groups(all_imgs, 3)
    res = []
    for num, group in enumerate(imgs_groups):
        min_shape = sorted([(np.sum(i.size), i.size) for i in group])[-1][1]
        imgs_comb = np.hstack((np.asarray(i.resize(min_shape)) for i in group))

        imgs_comb = Image.fromarray(imgs_comb)
        res.append(imgs_comb)

    return res


def split_text(text, n_words=10):
    splitted = [
        s for s in text.split(' ')
    ]
    refactored_string = [' '.join(
        [s for s in splitted[n_words * i:n_words * (i + 1)]]
    ) for i in range(n_words)]

    result_string = '\n'.join(
        [s for s in refactored_string if s]
    )

    return result_string


def get_people_data(df_people):
    res = {}
    for person in tqdm(filter(lambda a: '[' in a, list(df_people))):
        try:
            fig, ax = plt.subplots()
            plt.subplots_adjust(top=0.85)

            x = df_people[person].dropna().to_numpy()
            n_bins = 5
            n, bins, patches = ax.hist(x, bins=n_bins, edgecolor='black')
            ticks = [(patch._x0 + patch._x0 + patch._width) / 2
                     for patch in patches]
            ticklabels = [i + 1 for i in range(n_bins)]

            words_in_a_row = 6
            ax.set_xticks(ticks)
            ax.set_xticklabels(ticklabels)
            ax.set_title(split_text(person, words_in_a_row))
            ax.set_xlabel('Оценка', fontsize=14)
            ax.set_ylabel('Количество', fontsize=14)
            fig.canvas.draw()

            # dir = os.path.join(main_path, 'people', norm_path(f"{person[:person.find('[')]}"))
            # Path(dir).mkdir(parents=True, exist_ok=True)
            # file_name = norm_path(person)

            if person[:person.find('[')] not in res:
                res[person[:person.find('[')]] = []

            res[person[:person.find('[')]].append(fig)

            # plt.savefig(f"{dir}/{file_name}.jpeg", dpi=200, bbox_inches='tight')
            plt.cla()
            plt.close(fig)

        except Exception as e:
            print(e)

    for person, images in tqdm(res.items()):
        dir = os.path.join(main_path, 'people', norm_path(f"{person}"))
        Path(dir).mkdir(parents=True, exist_ok=True)

        for i, combined_images in enumerate(merge_images(images)):
            file_name = norm_path(f'{i}.jpeg')
            combined_images.save(f"{dir}/{file_name}.jpeg", dpi=(50, 50))


def get_subjects_data(df_subjects):
    res = {}
    for i in list(df_subjects):
        subj = re.search(r'\[(.*?)\]', i)
        if subj:
            subject = subj.group(1)
            
            try:
                fig, ax = plt.subplots()
                plt.subplots_adjust(top=0.85)


                x = df_subjects[i].dropna().to_numpy()
                n_bins = 5
                n, bins, patches = ax.hist(x, bins=n_bins, edgecolor='black')
                ticks = [(patch._x0 + patch._x0 + patch._width)/2 for patch in patches]
                ticklabels = [i + 1 for i in range(n_bins)]

                words_in_a_row = 6
                ax.set_xticks(ticks)
                ax.set_xticklabels(ticklabels)
                ax.set_title(split_text(i, words_in_a_row))
                ax.set_xlabel('Оценка', fontsize=14)
                ax.set_ylabel('Количество', fontsize=14)
                fig.canvas.draw()

                # subject_path = os.path.join(main_path, 'subjects', norm_path(subject))
                #
                # i_path = norm_path(i)
                # Path(f"{subject_path}").mkdir(parents=True, exist_ok=True)
                # plt.savefig(f"{subject_path}/{i_path[0:20]}.jpeg", dpi=200, bbox_inches='tight')

                if subject not in res:
                    res[subject] = []

                res[subject].append(fig)

                plt.cla()
                plt.close(fig)

            except Exception as e:
                print(e)

    for subject, images in tqdm(res.items()):
        dir = os.path.join(main_path, 'subjects', norm_path(f"{subject}"))
        Path(dir).mkdir(parents=True, exist_ok=True)

        for i, combined_images in enumerate(merge_images(images)):
            file_name = norm_path(f'{i}.jpeg')
            combined_images.save(f"{dir}/{file_name}.jpeg", dpi=(50, 50))
