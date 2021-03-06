package shadowbotz.shadowbotz.Controller;

import android.app.Activity;
import android.util.Log;
import android.widget.TextView;
import android.widget.Toast;

import shadowbotz.shadowbotz.Model.Robot;
import shadowbotz.shadowbotz.View.MainActivity;

import static android.content.ContentValues.TAG;

public class MovementController {
    ImageAdapter imageAdapter;
    Activity callingActivity;

    public MovementController(ImageAdapter imageAdapter, Activity callingActivity) {
        this.imageAdapter = imageAdapter;
        this.callingActivity = callingActivity;
    }

    private void checkIfWaypointIsExplored(Robot robot){
        if (!robot.isVisitedWaypoint()) {
            if(     robot.getWaypointPosition() == robot.getBody()-14 ||
                    robot.getWaypointPosition() == robot.getBody()-16 ||
                    robot.getWaypointPosition() == robot.getBody()+14 ||
                    robot.getWaypointPosition() == robot.getBody()+16 ||
                    robot.getWaypointPosition() == robot.getBody()+1 ||
                    robot.getWaypointPosition() == robot.getBody()-1 ||
                    robot.getWaypointPosition() == robot.getBody()+15 ||
                    robot.getWaypointPosition() == robot.getBody()-15 ||
                    robot.getWaypointPosition() == robot.getBody()){

                robot.setVisitedWaypoint(true);
                imageAdapter.mThumbIds[robot.getWaypointPosition()] = 11;
            }
        }
        else{
            imageAdapter.mThumbIds[robot.getWaypointPosition()] = 11;
        }

    }

    public void setBody(Robot robot){
        imageAdapter.mThumbIds[robot.getBody()] = 8;
        //4 corners
        imageAdapter.mThumbIds[robot.getBody()-14] = 8; //set the whole body
        imageAdapter.mThumbIds[robot.getBody()-16] = 8;
        imageAdapter.mThumbIds[robot.getBody()+14] = 8;
        imageAdapter.mThumbIds[robot.getBody()+16] = 8;

        //the rest
        imageAdapter.mThumbIds[robot.getBody()+1] = 8;
        imageAdapter.mThumbIds[robot.getBody()-1] = 8;
        imageAdapter.mThumbIds[robot.getBody()+15] = 8;
        imageAdapter.mThumbIds[robot.getBody()-15] = 8;
        imageAdapter.notifyDataSetChanged();
    }

    public void setHead(Robot robot){
        imageAdapter.mThumbIds[robot.getHead()] = 9;
        imageAdapter.notifyDataSetChanged();
//        robot.setWaypointPosition(-1); //to indicate no waypoint
    }

    public void clearRobot(Robot robot){
        checkRobotTrail(robot.getBody());
        //4 corners
        checkRobotTrail(robot.getBody()-14); //set the whole body
        checkRobotTrail(robot.getBody()-16);
        checkRobotTrail(robot.getBody()+14);
        checkRobotTrail(robot.getBody()+16);

        //the rest
        checkRobotTrail(robot.getBody()+1);
        checkRobotTrail(robot.getBody()-1);
        checkRobotTrail(robot.getBody()+15);
        checkRobotTrail(robot.getBody()-15);

//        robot.setBody(-1);
//        robot.setHead(-1);

        imageAdapter.notifyDataSetChanged();
    }

    public void clearWayPoint(Robot robot){
        checkRobotTrail(robot.getWaypointPosition());
//        robot.setWaypointPosition(-1);
        imageAdapter.notifyDataSetChanged();
    }

    public void setWayPoint(Robot robot, TextView statusTextView) {
        if(imageAdapter.currentMapWithNoRobot[robot.getWaypointPosition()] == 1){
            imageAdapter.mThumbIds[robot.getWaypointPosition()] = 11; //unexplored waypoint
        }
        else{
            imageAdapter.mThumbIds[robot.getWaypointPosition()] = 10; //unexplored waypoint
        }
        statusTextView.setText("Way point: "+robot.getWaypointPosition()%15+", "+Math.abs(19-(Math.abs(robot.getWaypointPosition()/15))));

        imageAdapter.notifyDataSetChanged();
    }

    private int turnRightwhenFaceRight(Robot robot){
        imageAdapter.mThumbIds[robot.getHead()] = 8;
        robot.setHead(robot.getBody()+15);
        imageAdapter.mThumbIds[robot.getHead()] = 9;
        imageAdapter.notifyDataSetChanged();
        return robot.getHead();
    }
    private int turnRightwhenFaceLeft(Robot robot){
        imageAdapter.mThumbIds[robot.getHead()] = 8;
        robot.setHead(robot.getBody()-15);
        imageAdapter.mThumbIds[robot.getHead()] = 9;
        imageAdapter.notifyDataSetChanged();
        return robot.getHead();
    }
    private int turnRightwhenFaceUp(Robot robot){
        imageAdapter.mThumbIds[robot.getHead()] = 8;
        robot.setHead(robot.getBody()+1);
        imageAdapter.mThumbIds[robot.getHead()] = 9;
        imageAdapter.notifyDataSetChanged();
        return robot.getHead();
    }
    private int turnRightwhenFaceDown(Robot robot){
        imageAdapter.mThumbIds[robot.getHead()] = 8;
        robot.setHead(robot.getBody()-1);
        imageAdapter.mThumbIds[robot.getHead()] = 9;
        imageAdapter.notifyDataSetChanged();
        return robot.getHead();
    }


    private int turnLeftwhenFaceRight(Robot robot){
        imageAdapter.mThumbIds[robot.getHead()] = 8;
        robot.setHead(robot.getBody()-15);
        imageAdapter.mThumbIds[robot.getHead()] = 9;
        imageAdapter.notifyDataSetChanged();
        return robot.getHead();
    }
    private int turnLeftwhenFaceLeft(Robot robot){
        imageAdapter.mThumbIds[robot.getHead()] = 8;
        robot.setHead(robot.getBody()+15);
        imageAdapter.mThumbIds[robot.getHead()] = 9;
        imageAdapter.notifyDataSetChanged();
        return robot.getHead();
    }
    private int turnLeftwhenFaceUp(Robot robot){
        imageAdapter.mThumbIds[robot.getHead()] = 8;
        robot.setHead(robot.getBody()-1);
        imageAdapter.mThumbIds[robot.getHead()] = 9;
        imageAdapter.notifyDataSetChanged();
        return robot.getHead();
    }
    private int turnLeftwhenFaceDown(Robot robot){
        imageAdapter.mThumbIds[robot.getHead()] = 8;
        robot.setHead(robot.getBody()+1);
        imageAdapter.mThumbIds[robot.getHead()] = 9;
        imageAdapter.notifyDataSetChanged();
        return robot.getHead();
    }

    private void moveForwardWhenFaceRight(Robot robot){
        imageAdapter.mThumbIds[robot.getHead()+1] = 9;

        //4 corners
        imageAdapter.mThumbIds[(robot.getBody()-14)+1] = 8; //set the whole body
        imageAdapter.mThumbIds[(robot.getBody()-16)+1] = 8;
        imageAdapter.mThumbIds[(robot.getBody()+14)+1] = 8;
        imageAdapter.mThumbIds[(robot.getBody()+16)+1] = 8;

        //the rest
        imageAdapter.mThumbIds[(robot.getBody())+1] = 8;
        imageAdapter.mThumbIds[(robot.getBody()-1)+1] = 8;
        imageAdapter.mThumbIds[(robot.getBody()+15)+1] = 8;
        imageAdapter.mThumbIds[(robot.getBody()-15)+1] = 8;

        //convert back of robot to explored
        checkRobotTrail((robot.getBody()-1));
        checkRobotTrail((robot.getBody()-16));
        checkRobotTrail((robot.getBody()+14));
    }

    private void moveForwardWhenFaceLeft(Robot robot){
        imageAdapter.mThumbIds[robot.getHead()-1] = 9;

        //4 corners
        imageAdapter.mThumbIds[(robot.getBody()-14)-1] = 8; //set the whole body
        imageAdapter.mThumbIds[(robot.getBody()-16)-1] = 8;
        imageAdapter.mThumbIds[(robot.getBody()+14)-1] = 8;
        imageAdapter.mThumbIds[(robot.getBody()+16)-1] = 8;

        //the rest
        imageAdapter.mThumbIds[(robot.getBody())-1] = 8;
        imageAdapter.mThumbIds[(robot.getBody()+1)-1] = 8;
        imageAdapter.mThumbIds[(robot.getBody()+15)-1] = 8;
        imageAdapter.mThumbIds[(robot.getBody()-15)-1] = 8;

        //convert back of robot to explored
        checkRobotTrail((robot.getBody()+1));
        checkRobotTrail((robot.getBody()+16));
        checkRobotTrail((robot.getBody()-14));
    }

    private void moveForwardWhenFaceUp(Robot robot){
        imageAdapter.mThumbIds[robot.getHead()-15] = 9;

        //4 corners
        imageAdapter.mThumbIds[(robot.getBody()-14)-15] = 8; //set the whole body
        imageAdapter.mThumbIds[(robot.getBody()-16)-15] = 8;
        imageAdapter.mThumbIds[(robot.getBody()+14)-15] = 8;
        imageAdapter.mThumbIds[(robot.getBody()+16)-15] = 8;

        //the rest
        imageAdapter.mThumbIds[(robot.getBody())-15] = 8;
        imageAdapter.mThumbIds[(robot.getBody()-1)-15] = 8;
        imageAdapter.mThumbIds[(robot.getBody()+15)-15] = 8;
        imageAdapter.mThumbIds[(robot.getBody()+1)-15] = 8;

        //convert back of robot to explored
        checkRobotTrail((robot.getBody()+14));
        checkRobotTrail((robot.getBody()+15));
        checkRobotTrail((robot.getBody()+16));
    }

    private void moveForwardWhenFaceDown(Robot robot){
        imageAdapter.mThumbIds[robot.getHead()+15] = 9;

        //4 corners
        imageAdapter.mThumbIds[(robot.getBody()-14)+15] = 8; //set the whole body
        imageAdapter.mThumbIds[(robot.getBody()-16)+15] = 8;
        imageAdapter.mThumbIds[(robot.getBody()+14)+15] = 8;
        imageAdapter.mThumbIds[(robot.getBody()+16)+15] = 8;

        //the rest
        imageAdapter.mThumbIds[(robot.getBody())+15] = 8;
        imageAdapter.mThumbIds[(robot.getBody()-1)+15] = 8;
        imageAdapter.mThumbIds[(robot.getBody()+1)+15] = 8;
        imageAdapter.mThumbIds[(robot.getBody()-15)+15] = 8;

        //convert back of robot to explored
        checkRobotTrail((robot.getBody()-14));
        checkRobotTrail((robot.getBody()-15));
        checkRobotTrail((robot.getBody()-16));
    }

    private void moveBackwardWhenFaceRight(Robot robot) {
        imageAdapter.mThumbIds[robot.getHead()-1] = 9;

        //4 corners
        imageAdapter.mThumbIds[(robot.getBody()-14)-1] = 8;
        imageAdapter.mThumbIds[(robot.getBody()-16)-1] = 8;
        imageAdapter.mThumbIds[(robot.getBody()+14)-1] = 8;
        imageAdapter.mThumbIds[(robot.getBody()+16)-1] = 8;

        //the rest
        imageAdapter.mThumbIds[(robot.getBody())-1] = 8;
        imageAdapter.mThumbIds[(robot.getBody()-1)-1] = 8;
        imageAdapter.mThumbIds[(robot.getBody()+15)-1] = 8;
        imageAdapter.mThumbIds[(robot.getBody()-15)-1] = 8;

        //convert back of robot to explored
        checkRobotTrail((robot.getBody()+1));
        checkRobotTrail((robot.getBody()+16));
        checkRobotTrail((robot.getBody()-14));
    }

    private void moveBackwardWhenFaceLeft(Robot robot){
        imageAdapter.mThumbIds[robot.getHead()+1] = 9;

        //4 corners
        imageAdapter.mThumbIds[(robot.getBody()-14)+1] = 8; //set the whole body
        imageAdapter.mThumbIds[(robot.getBody()-16)+1] = 8;
        imageAdapter.mThumbIds[(robot.getBody()+14)+1] = 8;
        imageAdapter.mThumbIds[(robot.getBody()+16)+1] = 8;

        //the rest
        imageAdapter.mThumbIds[(robot.getBody())+1] = 8;
        imageAdapter.mThumbIds[(robot.getBody()+1)+1] = 8;
        imageAdapter.mThumbIds[(robot.getBody()+15)+1] = 8;
        imageAdapter.mThumbIds[(robot.getBody()-15)+1] = 8;

        //convert back of robot to explored
        checkRobotTrail((robot.getBody()-1));
        checkRobotTrail((robot.getBody()-16));
        checkRobotTrail((robot.getBody()+14));
    }

    private void moveBackwardWhenFaceUp(Robot robot){
        imageAdapter.mThumbIds[robot.getHead()+15] = 9;

        //4 corners
        imageAdapter.mThumbIds[(robot.getBody()-14)+15] = 8;
        imageAdapter.mThumbIds[(robot.getBody()-16)+15] = 8;
        imageAdapter.mThumbIds[(robot.getBody()+14)+15] = 8;
        imageAdapter.mThumbIds[(robot.getBody()+16)+15] = 8;

        //the rest
        imageAdapter.mThumbIds[(robot.getBody())+15] = 8;
        imageAdapter.mThumbIds[(robot.getBody()-1)+15] = 8;
        imageAdapter.mThumbIds[(robot.getBody()+1)+15] = 8;
        imageAdapter.mThumbIds[(robot.getBody()+15)+15] = 8;

        //convert back of robot to explored
        checkRobotTrail((robot.getBody()-14));
        checkRobotTrail((robot.getBody()-15));
        checkRobotTrail((robot.getBody()-16));
    }

    private void moveBackwardWhenFaceDown(Robot robot){
        imageAdapter.mThumbIds[robot.getHead()-15] = 9;

        //4 corners
        imageAdapter.mThumbIds[(robot.getBody()-14)-15] = 8;
        imageAdapter.mThumbIds[(robot.getBody()-16)-15] = 8;
        imageAdapter.mThumbIds[(robot.getBody()+14)-15] = 8;
        imageAdapter.mThumbIds[(robot.getBody()+16)-15] = 8;

        //the rest
        imageAdapter.mThumbIds[(robot.getBody())-15] = 8;
        imageAdapter.mThumbIds[(robot.getBody()-1)-15] = 8;
        imageAdapter.mThumbIds[(robot.getBody()+1)-15] = 8;
        imageAdapter.mThumbIds[(robot.getBody()-15)-15] = 8;

        //convert back of robot to explored
        checkRobotTrail((robot.getBody()+14));
        checkRobotTrail((robot.getBody()+15));
        checkRobotTrail((robot.getBody()+16));
    }


    public void turnLeft(Robot robot){
        if(robot.getHead() == robot.getBody()+1){ //face right
            robot.setHead(turnLeftwhenFaceRight(robot));
        }
        else if(robot.getHead() == robot.getBody()-1) { //face left
            robot.setHead(turnLeftwhenFaceLeft(robot));
        }
        else if(robot.getHead() == robot.getBody()-15) { //face up
            robot.setHead(turnLeftwhenFaceUp(robot));
        }
        else{ //face down
            robot.setHead(turnLeftwhenFaceDown(robot));
        }
        checkIfWaypointIsExplored(robot);
        imageAdapter.notifyDataSetChanged();
    }


    public void turnRight(Robot robot){
        if(robot.getHead() == robot.getBody()+1){ //face right
            robot.setHead(turnRightwhenFaceRight(robot));
        }
        else if(robot.getHead() == robot.getBody()-1) { //face left
            robot.setHead(turnRightwhenFaceLeft(robot));

        }
        else if(robot.getHead() == robot.getBody()-15) { //face up

            robot.setHead(turnRightwhenFaceUp(robot));

        }
        else{ //face down
            robot.setHead(turnRightwhenFaceDown(robot));
        }
        checkIfWaypointIsExplored(robot);
        imageAdapter.notifyDataSetChanged();
    }

    public void moveForward(Robot robot){
        if((robot.getHead()%15>=1 && robot.getHead()%15<=13) && (Math.abs(robot.getHead()/15) >=1 && Math.abs(robot.getHead()/15) <=18)){
            if(robot.getHead() == robot.getBody()+1){ //face right
                moveForwardWhenFaceRight(robot);
                //increase current of head and body by 1 grid forward
                robot.setHead(robot.getHead()+1);
                robot.setBody(robot.getBody()+1);
            }
            else if(robot.getHead() == robot.getBody()-1){ //face left
                moveForwardWhenFaceLeft(robot);
                //increase current of head and body by 1 grid forward
                robot.setHead(robot.getHead()-1);
                robot.setBody(robot.getBody()-1);
            }
            else if(robot.getHead() == robot.getBody()-15){ //face up
                moveForwardWhenFaceUp(robot);
                //increase current of head and body by 1 grid forward
                robot.setHead(robot.getHead()-15);
                robot.setBody(robot.getBody()-15);
            }
            else{ //face down
                moveForwardWhenFaceDown(robot);
                //increase current of head and body by 1 grid forward
                robot.setHead(robot.getHead()+15);
                robot.setBody(robot.getBody()+15);
            }
            checkIfWaypointIsExplored(robot);
            imageAdapter.notifyDataSetChanged();
        }
        else{
            Toast.makeText(callingActivity, "Out of bound!", Toast.LENGTH_SHORT).show();
        }
    }

    public void moveBackward(Robot robot) {
        if (robot.getHead() == robot.getBody() + 1 && robot.getHead()%15 >= 3 && robot.getHead()%15 <= 14) { //face right
            moveBackwardWhenFaceRight(robot);
            //decrease current of head and body by 1 grid backward
            robot.setHead(robot.getHead() - 1);
            robot.setBody(robot.getBody() - 1);
            checkIfWaypointIsExplored(robot);
            imageAdapter.notifyDataSetChanged();
        } else if (robot.getHead() == robot.getBody() - 1 && robot.getHead()%15 >= 0 && robot.getHead()%15 <= 11) { //face left
            moveBackwardWhenFaceLeft(robot);
            //decrease current head and body by 1 grid backward
            robot.setHead(robot.getHead() + 1);
            robot.setBody(robot.getBody() + 1);
            checkIfWaypointIsExplored(robot);
            imageAdapter.notifyDataSetChanged();
        } else if (robot.getHead() == robot.getBody() - 15 && Math.abs(robot.getHead()/15) >= 0 && Math.abs(robot.getHead() / 15) <= 16) {//face up
            moveBackwardWhenFaceUp(robot);
            //decrease current head and body by 1 grid backward
            robot.setHead(robot.getHead() + 15);
            robot.setBody(robot.getBody() + 15);
            checkIfWaypointIsExplored(robot);
            imageAdapter.notifyDataSetChanged();
        } else if (robot.getHead() == robot.getBody() + 15 && Math.abs(robot.getHead()/15)>=3 && Math.abs((robot.getHead()/15))<=19) {//face down
            moveBackwardWhenFaceDown(robot);
            //decrease current head and body by 1 grid backward
            robot.setHead(robot.getHead() - 15);
            robot.setBody(robot.getBody() - 15);
            checkIfWaypointIsExplored(robot);
            imageAdapter.notifyDataSetChanged();
        } else {
            Toast.makeText(callingActivity, "Out of bound!", Toast.LENGTH_SHORT).show();
        }
    }


    public void checkRobotTrail(int position){
        if(imageAdapter.currentMapWithNoRobot[position] == 0){ //unexplored
            imageAdapter.mThumbIds[position] =0;
        }
        else if(imageAdapter.currentMapWithNoRobot[position] == 1){ //explored
            imageAdapter.mThumbIds[position] =1;
        }
        else if(imageAdapter.currentMapWithNoRobot[position] == 2){ //obstacle
            imageAdapter.mThumbIds[position] =2;
        }
        else if(imageAdapter.currentMapWithNoRobot[position] == 3){ //arrow
            imageAdapter.mThumbIds[position] =3;
        }
        else if(imageAdapter.currentMapWithNoRobot[position] == 4){ //arrow
            imageAdapter.mThumbIds[position] =4;
        }
        else if(imageAdapter.currentMapWithNoRobot[position] == 5){ //arrow
            imageAdapter.mThumbIds[position] =5;
        }
        else if(imageAdapter.currentMapWithNoRobot[position] == 6){ //arrow
            imageAdapter.mThumbIds[position] =6;
        }
        else if(imageAdapter.currentMapWithNoRobot[position] == 10){ //unexplored waypoint
            imageAdapter.mThumbIds[position] =10;
        }

        else if(imageAdapter.currentMapWithNoRobot[position] == 11){ //explored waypoint
            imageAdapter.mThumbIds[position] =11;
        }

    }

}
