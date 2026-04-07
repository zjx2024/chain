package com.example.industryriskassessmentserver.mapper;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.example.industryriskassessmentserver.entity.TrainingTask;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Select;
import org.apache.ibatis.annotations.Update;

import java.util.List;

@Mapper
public interface TrainingTaskMapper extends BaseMapper<TrainingTask> {
    
    /**
     * 获取正在运行的训练任务列表
     */
    @Select("SELECT * FROM training_task WHERE status = 'RUNNING' ORDER BY start_time DESC")
    List<TrainingTask> getRunningTasks();
    
    /**
     * 获取最近的训练任务列表（包含所有状态）
     */
    @Select("SELECT * FROM training_task ORDER BY create_time DESC LIMIT #{limit}")
    List<TrainingTask> getRecentTasks(int limit);
    
    /**
     * 更新训练任务的当前轮次
     */
    @Update("UPDATE training_task SET current_epoch = #{currentEpoch}, update_time = NOW() WHERE id = #{id}")
    int updateCurrentEpoch(Long id, Integer currentEpoch);
    
    /**
     * 更新训练任务状态
     */
    @Update("UPDATE training_task SET status = #{status}, end_time = #{endTime}, update_time = NOW() WHERE id = #{id}")
    int updateTaskStatus(Long id, String status, String endTime);
} 