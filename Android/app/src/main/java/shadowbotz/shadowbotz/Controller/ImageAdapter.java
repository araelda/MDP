package shadowbotz.shadowbotz.Controller;

import android.content.Context;
import android.view.View;
import android.view.ViewGroup;
import android.widget.BaseAdapter;
import android.widget.GridView;
import android.widget.ImageView;


import shadowbotz.shadowbotz.R;

public class ImageAdapter extends BaseAdapter {
    private Context mContext;

    public ImageAdapter(Context c) {
        mContext = c;
    }

    public int getCount() {
        return mThumbIds.length;
    }

    public Object getItem(int position) {
        return null;
    }

    public long getItemId(int position) {
        return 0;
    }

    // create a new ImageView for each item referenced by the Adapter
    public View getView(int position, View convertView, ViewGroup parent) {
        ImageView imageView;
        if (convertView == null) {
            // if it's not recycled, initialize some attributes
            imageView = new ImageView(mContext);

        } else {
            imageView = (ImageView) convertView;
        }

        switch(mThumbIds[position]){
            case 0: //unexplored
                imageView.setImageResource(R.drawable.tile);
                break;
            case 1: //explored
                imageView.setImageResource(R.drawable.tile_explored);
                break;
            case 2: //obstacle
                imageView.setImageResource(R.drawable.tile_obstacle);
                break;
                /* Legacy
            case 3: //up arrow
                imageView.setImageResource(R.drawable.tile_arrow_up);
                break;
            case 4://down arrow
                imageView.setImageResource(R.drawable.tile_arrow_down);
                break;
            case 5://left arrow
                imageView.setImageResource(R.drawable.tile_arrow_left);
                break;
            case 6://right arrow
                imageView.setImageResource(R.drawable.tile_arrow_right);
                break;
                 */
            case 8: //robot body tile
                imageView.setImageResource(R.drawable.tile_robot_body);
                break;
            case 9: //robot head tile
                imageView.setImageResource(R.drawable.tile_robot_head);
                break;
            case 10: //unexplore waypoint tile
                imageView.setImageResource(R.drawable.tile_waypoint_unexplored);
                break;
            case 11: //explore waypoint tile
                imageView.setImageResource(R.drawable.tile_waypoint_explored);
                break;
            case 12: //white arrow
                imageView.setImageResource(R.drawable.tile_arrow_white);
                break;
            case 13: //red arrow
                imageView.setImageResource(R.drawable.tile_arrow_red);
                break;
            case 14: //green arrow
                imageView.setImageResource(R.drawable.tile_arrow_green);
                break;
            case 15: //blue arrow
                imageView.setImageResource(R.drawable.tile_arrow_blue);
                break;
            case 16: //yellow circle
                imageView.setImageResource(R.drawable.tile_circle_yellow);
                break;
            case 17: //blue 1
                imageView.setImageResource(R.drawable.tile_one_blue);
                break;
            case 18: //green 2
                imageView.setImageResource(R.drawable.tile_two_green);
                break;
            case 19: //red 3
                imageView.setImageResource(R.drawable.tile_three_red);
                break;
            case 20: //white 4
                imageView.setImageResource(R.drawable.tile_four_white);
                break;
            case 21: //yellow 5
                imageView.setImageResource(R.drawable.tile_five_yellow);
                break;
            case 22: //red a
                imageView.setImageResource(R.drawable.tile_a_red);
                break;
            case 23: //green b
                imageView.setImageResource(R.drawable.tile_b_green);
                break;
            case 24: //white c
                imageView.setImageResource(R.drawable.tile_c_white);
                break;
            case 25: //blue d
                imageView.setImageResource(R.drawable.tile_d_blue);
                break;
            case 26: //yellow e
                imageView.setImageResource(R.drawable.tile_e_yellow);
                break;
        }
        //imageView.setLayoutParams(new ViewGroup.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.MATCH_PARENT));
        imageView.setPadding(0, 0, 0, 0);
        imageView.setAdjustViewBounds(true);
        imageView.setScaleType(ImageView.ScaleType.CENTER_CROP);
        return imageView;
    }

    // references to our images
    public Integer[] mThumbIds = {
            0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};

    public Integer[] currentMapWithNoRobot = {
            0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};
}