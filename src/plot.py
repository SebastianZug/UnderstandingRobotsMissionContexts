import pandas as pd
import matplotlib.pyplot as plt
import math

def plot_tracks(ax, id, reference_by_id, df_tracks, df_robot, df_orientations):

    if reference_by_id:
        df_id = df_tracks[(df_tracks['obj.label_id_unique'] == id) & 
                      (df_tracks['pose_valid'])]
    else:
        df_id = df_tracks[(df_tracks['obj.label_id_width_date'] == id) & 
                        (df_tracks['pose_valid'])]

    for index, row in df_id.iterrows():
            ax.plot([row['robot_longitude'], row['longitude_human']], 
            [row['robot_latitude'], row['latitude_human']], '-', 
            color = 'gray', alpha=0.2)

    ax.plot(df_id['longitude_human'], df_id['latitude_human'], 
                color='green', marker = 'o')

    ax.text(x=0, y=1.05, s=f"Track {id}", fontsize=8, transform=ax.transAxes)

    if reference_by_id:
        aux= df_orientations[df_orientations["obj.label_id_unique"]==id]
    else:
        aux= df_orientations[df_orientations["obj.label_id_width_date"]==id]

    ax.plot([aux.robot_begin_longitude.values[0],
                aux.robot_end_longitude.values[0]],
                [aux.robot_begin_latitude.values[0],
                aux.robot_end_latitude.values[0]],
                color='blue')
        
    ax.plot([aux.human_begin_longitude.values[0],
                aux.human_end_longitude.values[0]],
                [aux.human_begin_latitude.values[0],
                aux.human_end_latitude.values[0]],
                color='black', linestyle='--')

    #if aux.human_speed_est.values[0] < 0.4:
    #        ax.set_facecolor("yellow")

    #plt.text(0.7, 0.5, f"$r_h$={aux.human_corr_coeff.values[0]:.2f}",
    #        horizontalalignment='center',
    #        verticalalignment='center',
    #        transform = ax.transAxes)
    text = f"$angle$={aux.angle_robot_human.values[0]:.2f}"
    print(text)
    plt.text(0.7, 0.1, text,
            horizontalalignment='center',
            verticalalignment='center',
            transform = ax.transAxes)

    # Robots movements
    df_robot_tracks = df_robot[(df_robot['timestamp'] >= df_id['gnss.timestamp'].min()) & \
                                (df_robot['timestamp'] <= df_id['gnss.timestamp'].max())]

    df_robot_tracks[df_robot_tracks['pose_valid']==False]\
                        .plot(x='longitude', y='latitude', 
                            ax=ax, label='invalid robot positions', 
                            color='red', marker='P', linestyle='None')

    df_robot_tracks[df_robot_tracks['pose_valid']]\
                .plot(x='longitude', y='latitude', 
                    ax=ax, label='gnss measurements robot', 
                    color='black', marker='o', linestyle='None')

    ax.plot(df_id.iloc[-1]['robot_longitude'], df_id.iloc[-1]['robot_latitude'],'or')
    ax.plot(df_id.iloc[-1]['longitude_human'], df_id.iloc[-1]['latitude_human'],'or')


    ax.set_aspect('equal', 'box')
    ax.get_legend().remove()
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlabel('')